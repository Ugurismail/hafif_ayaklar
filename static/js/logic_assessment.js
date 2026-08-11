(function () {
  'use strict';

  function safeParse(value, fallback) {
    try {
      return value ? JSON.parse(value) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function initializeAssessment(root) {
    var storageKey = 'hafifayaklar.logic.assessment.v1.' + root.dataset.attemptId;
    var state = safeParse(window.sessionStorage.getItem(storageKey), {answers: {}, checked: []});
    var modules = Array.from(root.querySelectorAll('[data-assessment-module]'));
    var questions = Array.from(root.querySelectorAll('[data-assessment-question]'));
    var passCorrect = Number(root.dataset.passCorrect || 0);

    function saveState() {
      try {
        window.sessionStorage.setItem(storageKey, JSON.stringify(state));
      } catch (error) {
        // The current page remains functional without session storage.
      }
    }

    function questionState(question) {
      var selected = question.querySelector('input[type="radio"]:checked');
      return {
        answered: Boolean(selected),
        correct: Boolean(selected && selected.value === question.dataset.correctIndex)
      };
    }

    function moduleState(module) {
      var moduleQuestions = Array.from(module.querySelectorAll('[data-assessment-question]'));
      var answered = moduleQuestions.filter(function (question) {
        return questionState(question).answered;
      }).length;
      var correct = moduleQuestions.filter(function (question) {
        return questionState(question).correct;
      }).length;
      return {
        total: moduleQuestions.length,
        answered: answered,
        correct: correct,
        complete: moduleQuestions.length > 0 && answered === moduleQuestions.length,
        percent: moduleQuestions.length ? Math.round((correct / moduleQuestions.length) * 100) : 0
      };
    }

    function setText(selector, value) {
      root.querySelectorAll(selector).forEach(function (target) {
        target.textContent = value;
      });
    }

    function updateSummary() {
      var answered = questions.filter(function (question) {
        return questionState(question).answered;
      }).length;
      var checkedModules = modules.filter(function (module) {
        return state.checked.indexOf(module.dataset.assessmentModule) !== -1;
      });
      var correct = checkedModules.reduce(function (total, module) {
        return total + moduleState(module).correct;
      }, 0);
      var completedModules = checkedModules.filter(function (module) {
        return moduleState(module).complete;
      }).length;
      var percent = questions.length ? Math.round((correct / questions.length) * 100) : 0;
      var allComplete = completedModules === modules.length;
      var status = allComplete ? (correct >= passCorrect ? 'Ustalık eşiği aşıldı' : 'Tekrar öneriliyor') : 'Devam ediyor';
      var weakest = checkedModules.map(function (module) {
        return {module: module, result: moduleState(module)};
      }).filter(function (item) {
        return item.result.answered > 0;
      }).sort(function (left, right) {
        return left.result.percent - right.result.percent;
      })[0];

      setText('[data-assessment-correct]', String(correct));
      setText('[data-assessment-answered]', String(answered));
      setText('[data-assessment-completed]', String(completedModules));
      setText('[data-assessment-percent]', '%' + percent);
      setText('[data-assessment-status]', status);
      var progress = root.querySelector('[data-assessment-progress]');
      if (progress) {
        progress.parentElement.style.setProperty('--progress', percent + '%');
      }

      var recommendation = root.querySelector('[data-assessment-recommendation]');
      if (recommendation) {
        if (!weakest) {
          recommendation.textContent = 'Önce ilk modülü tamamla.';
        } else if (allComplete && correct >= passCorrect) {
          recommendation.textContent = 'Çekirdek yeterlik sağlandı. Yanlış yanıtların açıklamalarını gözden geçir.';
        } else {
          var title = weakest.module.querySelector('.logic-assessment-module-title strong');
          recommendation.textContent = 'Öncelik: ' + title.textContent + ' (%' + weakest.result.percent + ').';
        }
      }

      modules.forEach(function (module) {
        var result = moduleState(module);
        var nav = root.querySelector('[data-assessment-module-link="' + module.dataset.assessmentModule + '"]');
        if (nav) {
          nav.classList.toggle('is-completed', result.complete);
          var icon = nav.querySelector('[data-module-nav-status]');
          if (icon) {
            icon.className = result.complete ? 'bi bi-check-circle-fill' : 'bi bi-circle';
            icon.dataset.moduleNavStatus = '';
          }
        }
      });
    }

    function gradeModule(module, reveal) {
      var moduleQuestions = Array.from(module.querySelectorAll('[data-assessment-question]'));
      moduleQuestions.forEach(function (question) {
        var selected = question.querySelector('input[type="radio"]:checked');
        var feedback = question.querySelector('.logic-feedback');
        var title = question.querySelector('[data-feedback-title]');
        question.querySelectorAll('.logic-choice').forEach(function (choice) {
          choice.classList.remove('is-correct-choice', 'is-wrong-choice');
        });
        feedback.classList.remove('is-correct', 'is-wrong');

        if (!reveal) {
          return;
        }
        if (!selected) {
          feedback.classList.add('is-wrong');
          title.textContent = 'Bu soru boş bırakıldı.';
          return;
        }
        var selectedChoice = selected.closest('.logic-choice');
        var correctInput = question.querySelector('input[value="' + question.dataset.correctIndex + '"]');
        if (selected.value === question.dataset.correctIndex) {
          selectedChoice.classList.add('is-correct-choice');
          feedback.classList.add('is-correct');
          title.textContent = 'Doğru.';
        } else {
          selectedChoice.classList.add('is-wrong-choice');
          if (correctInput) {
            correctInput.closest('.logic-choice').classList.add('is-correct-choice');
          }
          feedback.classList.add('is-wrong');
          title.textContent = 'Yanlış.';
        }
      });

      var result = moduleState(module);
      var score = module.querySelector('[data-module-score]');
      var resultText = module.querySelector('[data-module-result]');
      if (score) {
        score.textContent = reveal
          ? result.correct + '/' + result.total + ' doğru'
          : 'Yanıt değişti · yeniden değerlendir';
      }
      if (resultText) {
        resultText.textContent = reveal
          ? (result.answered < result.total
            ? (result.total - result.answered) + ' soru boş kaldı.'
            : '%' + result.percent + ' başarı.')
          : 'Sonucu görmek için modülü yeniden değerlendir.';
      }
      if (reveal && state.checked.indexOf(module.dataset.assessmentModule) === -1) {
        state.checked.push(module.dataset.assessmentModule);
      }
      saveState();
      updateSummary();
    }

    questions.forEach(function (question) {
      var savedValue = state.answers[question.dataset.assessmentQuestion];
      if (savedValue === undefined) {
        return;
      }
      var input = question.querySelector('input[value="' + savedValue + '"]');
      if (input) {
        input.checked = true;
      }
    });

    root.addEventListener('change', function (event) {
      var input = event.target.closest('[data-assessment-question] input[type="radio"]');
      if (!input) {
        return;
      }
      var question = input.closest('[data-assessment-question]');
      var module = input.closest('[data-assessment-module]');
      state.answers[question.dataset.assessmentQuestion] = input.value;
      var checkedIndex = state.checked.indexOf(module.dataset.assessmentModule);
      if (checkedIndex !== -1) {
        state.checked.splice(checkedIndex, 1);
        gradeModule(module, false);
      }
      saveState();
      updateSummary();
    });

    modules.forEach(function (module) {
      var button = module.querySelector('[data-check-module]');
      if (button) {
        button.addEventListener('click', function () {
          gradeModule(module, true);
        });
      }
      if (state.checked.indexOf(module.dataset.assessmentModule) !== -1) {
        gradeModule(module, true);
      }
    });

    root.querySelectorAll('[data-assessment-module-link]').forEach(function (link) {
      link.addEventListener('click', function (event) {
        var module = root.querySelector(link.getAttribute('href'));
        if (!module) {
          return;
        }
        event.preventDefault();
        module.open = true;
        module.scrollIntoView({behavior: 'smooth', block: 'start'});
        root.querySelectorAll('[data-assessment-module-link]').forEach(function (item) {
          item.classList.toggle('is-current', item === link);
        });
      });
    });

    var checkAll = root.querySelector('[data-check-all-modules]');
    if (checkAll) {
      checkAll.addEventListener('click', function () {
        modules.forEach(function (module) {
          module.open = true;
          gradeModule(module, true);
        });
      });
    }

    var reset = root.querySelector('[data-reset-assessment]');
    if (reset) {
      reset.addEventListener('click', function () {
        if (Object.keys(state.answers).length && !window.confirm('Bu test oturumundaki bütün seçimlerin temizlensin mi?')) {
          return;
        }
        state = {answers: {}, checked: []};
        window.sessionStorage.removeItem(storageKey);
        questions.forEach(function (question) {
          question.querySelectorAll('input[type="radio"]').forEach(function (input) {
            input.checked = false;
          });
          question.querySelectorAll('.logic-choice').forEach(function (choice) {
            choice.classList.remove('is-correct-choice', 'is-wrong-choice');
          });
          question.querySelector('.logic-feedback').classList.remove('is-correct', 'is-wrong');
        });
        modules.forEach(function (module) {
          module.querySelector('[data-module-score]').textContent = 'Henüz değerlendirilmedi';
          module.querySelector('[data-module-result]').textContent = 'Yanıtların bu tarayıcı oturumunda korunur.';
        });
        updateSummary();
      });
    }

    var newAssessment = root.querySelector('[data-new-assessment]');
    if (newAssessment) {
      newAssessment.addEventListener('click', function (event) {
        if (Object.keys(state.answers).length && !window.confirm('Yeni soru karışımı mevcut test oturumunu kapatacak. Devam edilsin mi?')) {
          event.preventDefault();
        }
      });
    }

    updateSummary();
  }

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.querySelector('[data-logic-assessment]');
    if (root) {
      initializeAssessment(root);
    }
  });
})();
