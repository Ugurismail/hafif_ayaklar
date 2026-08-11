(function () {
  'use strict';

  function safeParse(value, fallback) {
    try {
      return value ? JSON.parse(value) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function readCookie(name) {
    var prefix = name + '=';
    var cookie = document.cookie.split(';').map(function (item) {
      return item.trim();
    }).find(function (item) {
      return item.indexOf(prefix) === 0;
    });
    return cookie ? decodeURIComponent(cookie.slice(prefix.length)) : '';
  }

  function readResponses(storageKey) {
    var stored = safeParse(window.localStorage.getItem(storageKey), {});
    return stored && typeof stored === 'object' ? stored : {};
  }

  function writeResponses(storageKey, responses) {
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(responses));
    } catch (error) {
      // The lesson remains usable if private browsing blocks local storage.
    }
  }

  function postProgress(root, action, score) {
    if (root.dataset.authenticated !== 'true') {
      return Promise.resolve(null);
    }

    var payload = {
      lesson_slug: root.dataset.lessonSlug,
      action: action
    };
    if (score !== undefined) {
      payload.score = score;
    }

    return window.fetch(root.dataset.progressUrl, {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': readCookie('csrftoken')
      },
      body: JSON.stringify(payload)
    }).then(function (response) {
      if (!response.ok) {
        throw new Error('İlerleme kaydedilemedi.');
      }
      return response.json();
    });
  }

  function setProgressUI(root, record) {
    var threshold = Number(root.dataset.masteryThreshold || 70);
    var status = record.status || 'not_started';
    var bestScore = Number(record.bestScore || record.best_score || 0);
    var label = root.querySelector('[data-logic-progress-label]');
    var detail = root.querySelector('[data-logic-progress-detail]');
    var bar = root.querySelector('[data-logic-lesson-progress-bar]');

    root.dataset.progressStatus = status;
    root.dataset.bestScore = String(bestScore);
    if (label) {
      label.textContent = status === 'completed' ? 'Tamamlandı' : 'Devam ediyor';
    }
    if (detail) {
      detail.textContent = bestScore
        ? 'En iyi alıştırma puanın %' + bestScore + '. Ustalık eşiği %' + threshold + '.'
        : 'Alıştırmayı tamamladığında ilerlemen güncellenecek.';
    }
    if (bar) {
      bar.parentElement.style.setProperty('--progress', bestScore + '%');
    }
  }

  function initializeToc(root) {
    var links = Array.from(root.querySelectorAll('[data-logic-toc-link]'));
    var sections = links.map(function (link) {
      return document.querySelector(link.getAttribute('href'));
    }).filter(Boolean);
    if (!links.length || !sections.length || !('IntersectionObserver' in window)) {
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      var visible = entries.filter(function (entry) {
        return entry.isIntersecting;
      }).sort(function (left, right) {
        return left.boundingClientRect.top - right.boundingClientRect.top;
      });
      if (!visible.length) {
        return;
      }
      var id = '#' + visible[0].target.id;
      links.forEach(function (link) {
        link.classList.toggle('is-active', link.getAttribute('href') === id);
      });
    }, {rootMargin: '-12% 0px -72% 0px', threshold: 0});

    sections.forEach(function (section) {
      observer.observe(section);
    });
  }

  function initializeLesson(root) {
    var progressApi = window.HafifLogicProgress;
    var lessonSlug = root.dataset.lessonSlug;
    var progressStorageKey = root.dataset.storageKey;
    var responseStorageKey = root.dataset.responseStorageKey;
    var responseStore = readResponses(responseStorageKey);
    var lessonResponses = responseStore[lessonSlug] || {answers: {}, production: {}};
    var cards = Array.from(root.querySelectorAll('[data-logic-practice-card]'));
    var productionFields = Array.from(root.querySelectorAll('[data-logic-production]'));
    var checkButton = root.querySelector('[data-logic-check-all]');
    var resetButton = root.querySelector('[data-logic-reset-practice]');
    var summary = root.querySelector('[data-logic-practice-summary]');
    var serverRecord = {
      status: root.dataset.progressStatus || 'not_started',
      bestScore: Number(root.dataset.bestScore || 0),
      attemptCount: Number(root.dataset.attemptCount || 0),
      lastOpened: Date.now()
    };
    var currentRecord = progressApi
      ? progressApi.update(lessonSlug, serverRecord, progressStorageKey)
      : serverRecord;

    if (currentRecord.status === 'not_started') {
      currentRecord.status = 'started';
      if (progressApi) {
        currentRecord = progressApi.update(lessonSlug, currentRecord, progressStorageKey);
      }
    }
    setProgressUI(root, currentRecord);
    postProgress(root, 'opened').catch(function () {
      var saveState = root.querySelector('[data-logic-save-state]');
      if (saveState) {
        saveState.textContent = 'Cihazda saklandı; hesap eşitlemesi bekliyor';
      }
    });

    cards.forEach(function (card) {
      var index = card.dataset.questionIndex;
      var savedAnswer = lessonResponses.answers[index];
      if (savedAnswer === undefined) {
        return;
      }
      var input = Array.from(card.querySelectorAll('input[type="radio"]')).find(function (item) {
        return item.value === savedAnswer;
      });
      if (input) {
        input.checked = true;
      }
    });

    root.addEventListener('change', function (event) {
      var input = event.target.closest('[data-logic-practice-card] input[type="radio"]');
      if (!input) {
        return;
      }
      var card = input.closest('[data-logic-practice-card]');
      lessonResponses.answers[card.dataset.questionIndex] = input.value;
      responseStore[lessonSlug] = lessonResponses;
      writeResponses(responseStorageKey, responseStore);
    });

    productionFields.forEach(function (field) {
      var index = field.dataset.logicProduction;
      field.value = lessonResponses.production[index] || '';
      field.addEventListener('input', function () {
        lessonResponses.production[index] = field.value;
        responseStore[lessonSlug] = lessonResponses;
        writeResponses(responseStorageKey, responseStore);
      });
    });

    if (checkButton) {
      checkButton.addEventListener('click', function () {
        var correctCount = 0;
        var unansweredCount = 0;

        cards.forEach(function (card) {
          var answer = card.dataset.answer;
          var selected = card.querySelector('input[type="radio"]:checked');
          var feedback = card.querySelector('.logic-feedback');
          var title = card.querySelector('[data-logic-feedback-title]');
          feedback.classList.remove('is-correct', 'is-wrong');

          if (!selected) {
            unansweredCount += 1;
            feedback.classList.add('is-wrong');
            title.textContent = 'Bu soru boş bırakıldı.';
          } else if (selected.value === answer) {
            correctCount += 1;
            feedback.classList.add('is-correct');
            title.textContent = 'Doğru.';
          } else {
            feedback.classList.add('is-wrong');
            title.textContent = 'Doğru cevap: ' + answer;
          }
        });

        var score = cards.length ? Math.round((correctCount / cards.length) * 100) : 0;
        var threshold = Number(root.dataset.masteryThreshold || 70);
        var nextStatus = score >= threshold ? 'completed' : 'started';
        var previousAttempts = Number(currentRecord.attemptCount || 0);
        currentRecord = progressApi ? progressApi.update(lessonSlug, {
          status: nextStatus,
          lastScore: score,
          bestScore: Math.max(Number(currentRecord.bestScore || 0), score),
          attemptCount: previousAttempts + 1,
          lastOpened: Date.now()
        }, progressStorageKey) : {
          status: nextStatus,
          bestScore: score,
          attemptCount: previousAttempts + 1
        };
        setProgressUI(root, currentRecord);

        if (summary) {
          summary.classList.add('is-visible');
          summary.innerHTML = '<strong>%'+ score + '</strong> · ' + correctCount + '/' + cards.length +
            ' doğru' + (unansweredCount ? ' · ' + unansweredCount + ' boş' : '') +
            (score >= threshold ? ' · Ders tamamlandı' : ' · Ustalık eşiği %' + threshold);
        }

        lessonResponses.lastScore = score;
        responseStore[lessonSlug] = lessonResponses;
        writeResponses(responseStorageKey, responseStore);
        postProgress(root, 'graded', score).then(function (payload) {
          if (payload) {
            setProgressUI(root, {
              status: payload.status,
              bestScore: payload.best_score,
              attemptCount: payload.attempt_count
            });
          }
        }).catch(function () {
          var saveState = root.querySelector('[data-logic-save-state]');
          if (saveState) {
            saveState.textContent = 'Sonuç cihazda saklandı; hesap eşitlemesi bekliyor';
          }
        });
        var firstFeedback = root.querySelector('.logic-feedback.is-wrong');
        if (firstFeedback) {
          firstFeedback.scrollIntoView({behavior: 'smooth', block: 'center'});
        }
      });
    }

    if (resetButton) {
      resetButton.addEventListener('click', function () {
        var hasAnswers = cards.some(function (card) {
          return Boolean(card.querySelector('input[type="radio"]:checked'));
        });
        if (hasAnswers && !window.confirm('Bu dersteki çoktan seçmeli yanıtların temizlensin mi?')) {
          return;
        }
        cards.forEach(function (card) {
          card.querySelectorAll('input[type="radio"]').forEach(function (input) {
            input.checked = false;
          });
          var feedback = card.querySelector('.logic-feedback');
          feedback.classList.remove('is-correct', 'is-wrong');
        });
        lessonResponses.answers = {};
        responseStore[lessonSlug] = lessonResponses;
        writeResponses(responseStorageKey, responseStore);
        if (summary) {
          summary.classList.remove('is-visible');
          summary.textContent = '';
        }
      });
    }

    initializeToc(root);
  }

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('[data-logic-lesson-page]');
    if (root) {
      initializeLesson(root);
    }
  });
})();
