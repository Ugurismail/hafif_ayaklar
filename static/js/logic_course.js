(function () {
  'use strict';

  var DEFAULT_STORAGE_KEY = 'hafifayaklar.logic.progress.v2';
  var STATUS_RANK = {not_started: 0, started: 1, completed: 2};

  function safeParse(value, fallback) {
    try {
      return value ? JSON.parse(value) : fallback;
    } catch (error) {
      return fallback;
    }
  }

  function readStore(storageKey) {
    var stored = safeParse(window.localStorage.getItem(storageKey), {});
    return stored && typeof stored === 'object' ? stored : {};
  }

  function writeStore(storageKey, data) {
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(data));
    } catch (error) {
      // Progress still works for the current page when storage is unavailable.
    }
  }

  function mergeRecord(existing, incoming) {
    var current = existing || {};
    var next = incoming || {};
    var currentStatus = current.status || 'not_started';
    var nextStatus = next.status || 'not_started';

    return {
      status: STATUS_RANK[nextStatus] > STATUS_RANK[currentStatus] ? nextStatus : currentStatus,
      bestScore: Math.max(Number(current.bestScore || 0), Number(next.bestScore || 0)),
      lastScore: Number(next.lastScore !== undefined ? next.lastScore : (current.lastScore || 0)),
      attemptCount: Math.max(Number(current.attemptCount || 0), Number(next.attemptCount || 0)),
      lastOpened: Math.max(Number(current.lastOpened || 0), Number(next.lastOpened || 0))
    };
  }

  function updateRecord(slug, incoming, storageKey) {
    var key = storageKey || DEFAULT_STORAGE_KEY;
    var store = readStore(key);
    store[slug] = mergeRecord(store[slug], incoming);
    writeStore(key, store);
    return store[slug];
  }

  function getRecord(slug, storageKey) {
    return readStore(storageKey || DEFAULT_STORAGE_KEY)[slug] || null;
  }

  function normalizeSearch(value) {
    return String(value || '')
      .toLocaleLowerCase('tr-TR')
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim();
  }

  function statusIcon(status) {
    if (status === 'completed') {
      return '<i class="bi bi-check-circle-fill"></i>';
    }
    if (status === 'started') {
      return '<i class="bi bi-circle-half"></i>';
    }
    return '<i class="bi bi-arrow-up-right"></i>';
  }

  function initializeCourse(root) {
    var storageKey = root.dataset.storageKey || DEFAULT_STORAGE_KEY;
    var lessonRows = Array.from(root.querySelectorAll('[data-logic-lesson]'));
    var stages = Array.from(root.querySelectorAll('.logic-stage'));
    var searchInput = root.querySelector('[data-logic-search]');
    var searchClear = root.querySelector('[data-logic-search-clear]');
    var filterButtons = Array.from(root.querySelectorAll('[data-logic-filter]'));
    var emptyState = root.querySelector('[data-logic-empty]');
    var activeFilter = 'all';
    var store = readStore(storageKey);

    lessonRows.forEach(function (row) {
      var slug = row.dataset.lessonSlug;
      var serverRecord = {
        status: row.dataset.status || 'not_started',
        bestScore: Number(row.dataset.bestScore || 0)
      };
      var merged = mergeRecord(serverRecord, store[slug]);
      store[slug] = merged;
      row.dataset.status = merged.status;
      row.dataset.bestScore = String(merged.bestScore);
      var icon = row.querySelector('[data-logic-status-icon]');
      if (icon) {
        icon.innerHTML = statusIcon(merged.status);
      }

      var foot = row.querySelector('.logic-lesson-foot');
      if (foot && merged.bestScore > 0 && !foot.querySelector('[data-local-best-score]')) {
        var score = document.createElement('span');
        score.dataset.localBestScore = '';
        score.textContent = 'En iyi: %' + merged.bestScore;
        foot.appendChild(score);
      }
    });
    writeStore(storageKey, store);

    function updateProgress() {
      var completed = lessonRows.filter(function (row) {
        return row.dataset.status === 'completed';
      }).length;
      var total = lessonRows.length;
      var percent = total ? Math.round((completed / total) * 100) : 0;
      var completedTarget = root.querySelector('[data-logic-completed]');
      var numberTarget = root.querySelector('[data-logic-progress-number]');
      var progressBar = root.querySelector('[data-logic-progress-bar]');

      if (completedTarget) {
        completedTarget.textContent = String(completed);
      }
      if (numberTarget) {
        numberTarget.textContent = '%' + percent;
      }
      if (progressBar) {
        progressBar.parentElement.style.setProperty('--progress', percent + '%');
      }

      stages.forEach(function (stage) {
        var rows = Array.from(stage.querySelectorAll('[data-logic-lesson]'));
        var stageCompleted = rows.filter(function (row) {
          return row.dataset.status === 'completed';
        }).length;
        var stagePercent = rows.length ? Math.round((stageCompleted / rows.length) * 100) : 0;
        var meta = stage.querySelector('.logic-stage-meta-line span:first-child');
        var bar = stage.querySelector('[data-stage-progress-bar]');
        if (meta) {
          meta.textContent = stageCompleted + '/' + rows.length + ' tamamlandı';
        }
        if (bar) {
          bar.parentElement.style.setProperty('--progress', stagePercent + '%');
        }
      });
    }

    function updateContinueLesson() {
      var continueBand = root.querySelector('[data-logic-continue]');
      if (!continueBand || !lessonRows.length) {
        return;
      }

      var incomplete = lessonRows.filter(function (row) {
        return row.dataset.status !== 'completed';
      });
      var started = incomplete.filter(function (row) {
        return row.dataset.status === 'started';
      });
      started.sort(function (left, right) {
        var leftOpened = (store[left.dataset.lessonSlug] || {}).lastOpened || 0;
        var rightOpened = (store[right.dataset.lessonSlug] || {}).lastOpened || 0;
        return rightOpened - leftOpened;
      });

      var target = started[0] || incomplete[0] || lessonRows[0];
      var title = target.querySelector('h4');
      var stage = target.closest('.logic-stage');
      var stageTitle = stage ? stage.querySelector('.logic-stage-title h3') : null;
      var duration = target.querySelector('.logic-lesson-foot span:first-child');
      var labelTarget = continueBand.querySelector('[data-logic-continue-label]');
      var titleTarget = continueBand.querySelector('[data-logic-continue-title]');
      var metaTarget = continueBand.querySelector('[data-logic-continue-meta]');
      var linkTarget = continueBand.querySelector('[data-logic-continue-link]');

      if (labelTarget) {
        labelTarget.textContent = target.dataset.status === 'started' ? 'Kaldığın yer' : 'Önerilen başlangıç';
      }
      if (titleTarget && title) {
        titleTarget.textContent = title.textContent;
      }
      if (metaTarget) {
        metaTarget.textContent = [
          stageTitle ? stageTitle.textContent : '',
          duration ? duration.textContent : ''
        ].filter(Boolean).join(' · ');
      }
      if (linkTarget) {
        linkTarget.href = target.href;
      }
    }

    function applyFilters() {
      var term = normalizeSearch(searchInput ? searchInput.value : '');
      var visibleCount = 0;

      lessonRows.forEach(function (row) {
        var matchesSearch = !term || normalizeSearch(row.dataset.searchText).includes(term);
        var matchesFilter = activeFilter === 'all' ||
          row.dataset.track === activeFilter ||
          row.dataset.status === activeFilter;
        var visible = matchesSearch && matchesFilter;
        row.hidden = !visible;
        visibleCount += Number(visible);
      });

      stages.forEach(function (stage) {
        var hasVisibleLesson = Array.from(stage.querySelectorAll('[data-logic-lesson]')).some(function (row) {
          return !row.hidden;
        });
        stage.hidden = !hasVisibleLesson;
        if (hasVisibleLesson && (term || activeFilter !== 'all')) {
          stage.open = true;
        }
      });

      if (emptyState) {
        emptyState.classList.toggle('is-visible', visibleCount === 0);
      }
    }

    if (searchInput) {
      searchInput.addEventListener('input', applyFilters);
    }
    if (searchClear) {
      searchClear.addEventListener('click', function () {
        if (!searchInput) {
          return;
        }
        searchInput.value = '';
        searchInput.focus();
        applyFilters();
      });
    }

    filterButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        activeFilter = button.dataset.logicFilter || 'all';
        filterButtons.forEach(function (item) {
          item.classList.toggle('is-active', item === button);
        });
        applyFilters();
      });
    });

    updateProgress();
    updateContinueLesson();
    applyFilters();
  }

  window.HafifLogicProgress = {
    defaultStorageKey: DEFAULT_STORAGE_KEY,
    get: getRecord,
    update: updateRecord,
    read: readStore
  };

  document.addEventListener('DOMContentLoaded', function () {
    var courseRoot = document.querySelector('[data-logic-course]');
    if (courseRoot) {
      initializeCourse(courseRoot);
    }
  });
})();
