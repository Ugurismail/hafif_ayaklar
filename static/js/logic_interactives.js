(function () {
  'use strict';

  var root = document.querySelector('[data-logic-interactive-root]');
  var configNode = document.getElementById('logic-interactive-config');
  var lessonPage = document.querySelector('[data-logic-lesson-page]');

  if (!root || !configNode || !lessonPage) {
    return;
  }

  var config;
  try {
    config = JSON.parse(configNode.textContent);
  } catch (error) {
    return;
  }

  var lessonSlug = lessonPage.dataset.lessonSlug || 'mantik-dersi';
  var storageKey = 'hafifayaklar.logic.labs.v2.' + lessonSlug;
  var statusNode = root.querySelector('[data-logic-lab-status]');
  var state = readState();

  function readState() {
    try {
      var stored = JSON.parse(window.localStorage.getItem(storageKey) || '{}');
      return stored.type === config.type ? stored : { type: config.type };
    } catch (error) {
      return { type: config.type };
    }
  }

  function saveState() {
    state.type = config.type;
    state.updatedAt = new Date().toISOString();
    try {
      window.localStorage.setItem(storageKey, JSON.stringify(state));
    } catch (error) {
      // The exercise still works when storage is unavailable.
    }
  }

  function setStatus(message, kind) {
    if (!statusNode) {
      return;
    }
    statusNode.textContent = message;
    statusNode.classList.toggle('is-complete', kind === 'complete');
    statusNode.classList.toggle('is-active', kind === 'active');
  }

  function touchLab(message) {
    if (state.completed) {
      setStatus('Tamamlandı', 'complete');
      return;
    }
    setStatus(message || 'Çalışma sürüyor', 'active');
  }

  function markLabComplete() {
    state.completed = true;
    root.classList.add('is-complete');
    setStatus('Tamamlandı', 'complete');
    saveState();
  }

  function setFeedback(node, message, kind) {
    if (!node) {
      return;
    }
    node.textContent = message;
    node.classList.add('is-visible');
    node.classList.toggle('is-success', kind === 'success');
    node.classList.toggle('is-warning', kind === 'warning');
  }

  function clearFeedback(node) {
    if (!node) {
      return;
    }
    node.textContent = '';
    node.classList.remove('is-visible', 'is-success', 'is-warning');
  }

  function arraysEqual(left, right) {
    return left.length === right.length && left.every(function (item, index) {
      return item === right[index];
    });
  }

  function initializeTruthTable(lab) {
    var cells = Array.from(lab.querySelectorAll('[data-truth-cell]'));
    var checkButton = lab.querySelector('[data-check-truth-table]');
    var resetButton = lab.querySelector('[data-reset-truth-table]');
    var summary = lab.querySelector('[data-truth-table-summary]');
    var values = ['', 'D', 'Y'];

    state.truthValues = Array.isArray(state.truthValues) ? state.truthValues : [];
    cells.forEach(function (cell, index) {
      var restored = values.includes(state.truthValues[index]) ? state.truthValues[index] : '';
      cell.dataset.value = restored;
      cell.textContent = restored || '-';
      cell.addEventListener('click', function () {
        var current = cell.dataset.value || '';
        var nextIndex = (values.indexOf(current) + 1) % values.length;
        cell.dataset.value = values[nextIndex];
        cell.textContent = values[nextIndex] || '-';
        cell.classList.remove('is-correct', 'is-wrong');
        state.truthValues[index] = values[nextIndex];
        clearFeedback(summary);
        touchLab();
        saveState();
      });
    });

    if (checkButton) {
      checkButton.addEventListener('click', function () {
        var correct = 0;
        var empty = 0;
        cells.forEach(function (cell) {
          var value = cell.dataset.value || '';
          cell.classList.remove('is-correct', 'is-wrong');
          if (!value) {
            empty += 1;
            cell.classList.add('is-wrong');
          } else if (value === cell.dataset.answer) {
            correct += 1;
            cell.classList.add('is-correct');
          } else {
            cell.classList.add('is-wrong');
          }
        });
        if (correct === cells.length) {
          setFeedback(summary, lab.dataset.successMessage, 'success');
          markLabComplete();
        } else {
          setFeedback(
            summary,
            correct + '/' + cells.length + ' doğru' + (empty ? ' · ' + empty + ' boş' : '') + '. ' + lab.dataset.reviewMessage,
            'warning'
          );
        }
      });
    }

    if (resetButton) {
      resetButton.addEventListener('click', function () {
        cells.forEach(function (cell) {
          cell.dataset.value = '';
          cell.textContent = '-';
          cell.classList.remove('is-correct', 'is-wrong');
        });
        state.truthValues = [];
        clearFeedback(summary);
        touchLab(state.completed ? 'Tamamlandı' : 'Başlamaya hazır');
        saveState();
      });
    }

    var completedTruthCellCount = state.truthValues.slice(0, cells.length).filter(Boolean).length;
    if (completedTruthCellCount && !state.completed) {
      setStatus(completedTruthCellCount + '/' + cells.length + ' hücre dolduruldu', 'active');
    }
  }

  function initializeSymbolization(lab) {
    var tasks = Array.from(lab.querySelectorAll('[data-symbol-task]'));
    state.symbolAnswers = Array.isArray(state.symbolAnswers) ? state.symbolAnswers : [];
    state.symbolCorrect = Array.isArray(state.symbolCorrect) ? state.symbolCorrect : [];

    function ensureTaskState(index) {
      if (!Array.isArray(state.symbolAnswers[index])) {
        state.symbolAnswers[index] = [];
      }
      state.symbolCorrect[index] = Boolean(state.symbolCorrect[index]);
    }

    function renderTask(taskElement, index) {
      ensureTaskState(index);
      var answerNode = taskElement.querySelector('[data-symbol-answer]');
      var feedback = taskElement.querySelector('[data-symbol-feedback]');
      var taskConfig = config.tasks[index];
      answerNode.replaceChildren();

      if (!state.symbolAnswers[index].length) {
        var empty = document.createElement('span');
        empty.className = 'logic-empty-formula';
        empty.textContent = 'Formülü aşağıdaki parçalardan kur';
        answerNode.appendChild(empty);
      } else {
        state.symbolAnswers[index].forEach(function (token, tokenIndex) {
          var tokenButton = document.createElement('button');
          tokenButton.type = 'button';
          tokenButton.className = 'logic-answer-token';
          tokenButton.textContent = token;
          tokenButton.title = 'Bu sembolü kaldır';
          tokenButton.setAttribute('aria-label', token + ' sembolünü formülden kaldır');
          tokenButton.addEventListener('click', function () {
            state.symbolAnswers[index].splice(tokenIndex, 1);
            state.symbolCorrect[index] = false;
            taskElement.classList.remove('is-correct', 'is-wrong');
            clearFeedback(feedback);
            touchLab();
            saveState();
            renderTask(taskElement, index);
          });
          answerNode.appendChild(tokenButton);
        });
      }

      taskElement.classList.toggle('is-correct', state.symbolCorrect[index]);
      if (state.symbolCorrect[index]) {
        setFeedback(feedback, taskConfig.success, 'success');
      }
    }

    tasks.forEach(function (taskElement, index) {
      ensureTaskState(index);
      var feedback = taskElement.querySelector('[data-symbol-feedback]');
      var taskConfig = config.tasks[index];

      taskElement.querySelectorAll('[data-symbol-token]').forEach(function (button) {
        button.addEventListener('click', function () {
          state.symbolAnswers[index].push(button.dataset.symbolToken);
          state.symbolCorrect[index] = false;
          taskElement.classList.remove('is-correct', 'is-wrong');
          clearFeedback(feedback);
          touchLab();
          saveState();
          renderTask(taskElement, index);
        });
      });

      taskElement.querySelector('[data-undo-symbol-task]').addEventListener('click', function () {
        state.symbolAnswers[index].pop();
        state.symbolCorrect[index] = false;
        taskElement.classList.remove('is-correct', 'is-wrong');
        clearFeedback(feedback);
        touchLab();
        saveState();
        renderTask(taskElement, index);
      });

      taskElement.querySelector('[data-clear-symbol-task]').addEventListener('click', function () {
        state.symbolAnswers[index] = [];
        state.symbolCorrect[index] = false;
        taskElement.classList.remove('is-correct', 'is-wrong');
        clearFeedback(feedback);
        touchLab();
        saveState();
        renderTask(taskElement, index);
      });

      taskElement.querySelector('[data-check-symbol-task]').addEventListener('click', function () {
        var candidate = state.symbolAnswers[index];
        var isCorrect = taskConfig.answers.some(function (answer) {
          return arraysEqual(candidate, answer);
        });
        state.symbolCorrect[index] = isCorrect;
        taskElement.classList.toggle('is-correct', isCorrect);
        taskElement.classList.toggle('is-wrong', !isCorrect);

        if (!candidate.length) {
          setFeedback(feedback, 'Önce sembolleri kullanarak bir formül kur.', 'warning');
        } else if (isCorrect) {
          setFeedback(feedback, taskConfig.success, 'success');
        } else {
          setFeedback(feedback, 'Formül henüz doğru değil. ' + taskConfig.hint, 'warning');
        }

        saveState();
        if (state.symbolCorrect.slice(0, tasks.length).every(Boolean)) {
          markLabComplete();
        } else {
          touchLab(state.symbolCorrect.filter(Boolean).length + '/' + tasks.length + ' görev tamamlandı');
        }
      });

      renderTask(taskElement, index);
    });

    var completedTaskCount = state.symbolCorrect.slice(0, tasks.length).filter(Boolean).length;
    if (completedTaskCount === tasks.length) {
      markLabComplete();
    } else if (completedTaskCount) {
      setStatus(completedTaskCount + '/' + tasks.length + ' görev tamamlandı', 'active');
    }
  }

  function initializeProofBuilder(lab) {
    var sequence = lab.querySelector('[data-proof-sequence]');
    var feedback = lab.querySelector('[data-proof-feedback]');
    var checkButton = lab.querySelector('[data-check-proof]');
    var undoButton = lab.querySelector('[data-undo-proof]');
    var resetButton = lab.querySelector('[data-reset-proof]');
    var candidateButtons = Array.from(lab.querySelectorAll('[data-proof-candidate]'));
    var stepById = {};

    config.steps.forEach(function (step) {
      stepById[step.id] = step;
    });
    state.proofOrder = Array.isArray(state.proofOrder)
      ? state.proofOrder.filter(function (id, index, values) {
          return stepById[id] && values.indexOf(id) === index;
        })
      : [];

    function resetValidation() {
      clearFeedback(feedback);
      sequence.querySelectorAll('.is-correct, .is-wrong').forEach(function (line) {
        line.classList.remove('is-correct', 'is-wrong');
      });
    }

    function moveStep(index, direction) {
      var target = index + direction;
      if (target < 0 || target >= state.proofOrder.length) {
        return;
      }
      var current = state.proofOrder[index];
      state.proofOrder[index] = state.proofOrder[target];
      state.proofOrder[target] = current;
      resetValidation();
      touchLab();
      saveState();
      renderSequence();
    }

    function renderSequence() {
      sequence.querySelectorAll('.logic-proof-line.is-user-step').forEach(function (line) {
        line.remove();
      });

      state.proofOrder.forEach(function (id, index) {
        var step = stepById[id];
        var line = document.createElement('li');
        line.className = 'logic-proof-line is-user-step';
        line.dataset.proofStepId = id;
        line.style.setProperty('--proof-depth', step.depth || 0);

        var number = document.createElement('span');
        number.textContent = config.premises.length + index + 1;
        var formula = document.createElement('strong');
        formula.textContent = step.formula;
        var rule = document.createElement('small');
        rule.textContent = step.rule;
        var controls = document.createElement('div');
        controls.className = 'logic-proof-line-controls';

        [
          { icon: 'bi-arrow-up', label: 'Satırı yukarı taşı', action: function () { moveStep(index, -1); }, disabled: index === 0 },
          { icon: 'bi-arrow-down', label: 'Satırı aşağı taşı', action: function () { moveStep(index, 1); }, disabled: index === state.proofOrder.length - 1 },
          { icon: 'bi-x-lg', label: 'Satırı kaldır', action: function () {
            state.proofOrder.splice(index, 1);
            resetValidation();
            touchLab();
            saveState();
            renderSequence();
          } },
        ].forEach(function (control) {
          var button = document.createElement('button');
          button.type = 'button';
          button.innerHTML = '<i class="bi ' + control.icon + '" aria-hidden="true"></i>';
          button.setAttribute('aria-label', control.label);
          button.title = control.label;
          button.disabled = Boolean(control.disabled);
          button.addEventListener('click', control.action);
          controls.appendChild(button);
        });

        line.append(number, formula, rule, controls);
        sequence.appendChild(line);
      });

      candidateButtons.forEach(function (button) {
        var used = state.proofOrder.includes(button.dataset.proofCandidate);
        button.disabled = used;
        button.classList.toggle('is-used', used);
      });
    }

    candidateButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var id = button.dataset.proofCandidate;
        if (!state.proofOrder.includes(id)) {
          state.proofOrder.push(id);
          resetValidation();
          touchLab();
          saveState();
          renderSequence();
        }
      });
    });

    checkButton.addEventListener('click', function () {
      resetValidation();
      var isCorrect = arraysEqual(state.proofOrder, config.answer_order);
      var userLines = Array.from(sequence.querySelectorAll('.logic-proof-line.is-user-step'));

      userLines.forEach(function (line, index) {
        line.classList.add(state.proofOrder[index] === config.answer_order[index] ? 'is-correct' : 'is-wrong');
      });

      if (isCorrect) {
        setFeedback(feedback, config.success, 'success');
        markLabComplete();
        return;
      }

      var mismatchIndex = 0;
      while (
        mismatchIndex < state.proofOrder.length &&
        state.proofOrder[mismatchIndex] === config.answer_order[mismatchIndex]
      ) {
        mismatchIndex += 1;
      }
      var expectedId = config.answer_order[mismatchIndex];
      var message;
      if (!state.proofOrder.length) {
        message = 'Önce aday satırlardan bir kanıt dizisi kur.';
      } else if (!expectedId) {
        message = 'Hedefe ulaştıktan sonra eklenen gereksiz veya lisanssız satırları kaldır.';
      } else {
        message = (config.premises.length + mismatchIndex + 1) + '. satırı yeniden düşün. ' + stepById[expectedId].hint;
      }
      setFeedback(feedback, message, 'warning');
      touchLab();
    });

    undoButton.addEventListener('click', function () {
      state.proofOrder.pop();
      resetValidation();
      touchLab();
      saveState();
      renderSequence();
    });

    resetButton.addEventListener('click', function () {
      state.proofOrder = [];
      resetValidation();
      touchLab(state.completed ? 'Tamamlandı' : 'Başlamaya hazır');
      saveState();
      renderSequence();
    });

    renderSequence();
    if (state.proofOrder.length && !state.completed) {
      setStatus(state.proofOrder.length + '/' + config.answer_order.length + ' adım yerleştirildi', 'active');
    }
  }

  function initializeModelBuilder(lab) {
    var challengeButtons = Array.from(lab.querySelectorAll('[data-model-challenge]'));
    var titleNode = lab.querySelector('[data-model-challenge-title]');
    var promptNode = lab.querySelector('[data-model-challenge-prompt]');
    var formulaNode = lab.querySelector('[data-model-formula]');
    var relationPanel = lab.querySelector('[data-model-relations]');
    var conditionList = lab.querySelector('[data-model-condition-list]');
    var feedback = lab.querySelector('[data-model-feedback]');
    var predicateButtons = Array.from(lab.querySelectorAll('[data-model-predicate]'));
    var relationButtons = Array.from(lab.querySelectorAll('[data-model-relation]'));
    var checkButton = lab.querySelector('[data-check-model]');
    var resetButton = lab.querySelector('[data-reset-model]');
    var objectIds = config.objects.map(function (item) { return item.id; });
    var predicateIds = config.predicates.map(function (item) { return item.id; });
    var relationIds = config.relations.map(function (item) { return item.id; });

    function blankChallengeState() {
      var assignments = {};
      var relations = {};
      objectIds.forEach(function (objectId) {
        assignments[objectId] = {};
        predicateIds.forEach(function (predicateId) {
          assignments[objectId][predicateId] = false;
        });
      });
      relationIds.forEach(function (relationId) {
        relations[relationId] = {};
        objectIds.forEach(function (sourceId) {
          objectIds.forEach(function (targetId) {
            relations[relationId][sourceId + ':' + targetId] = false;
          });
        });
      });
      return { assignments: assignments, relations: relations, completed: false, results: [] };
    }

    function normalizeChallengeState(candidate) {
      var normalized = blankChallengeState();
      if (!candidate || typeof candidate !== 'object') {
        return normalized;
      }
      objectIds.forEach(function (objectId) {
        predicateIds.forEach(function (predicateId) {
          normalized.assignments[objectId][predicateId] = Boolean(
            candidate.assignments && candidate.assignments[objectId] && candidate.assignments[objectId][predicateId]
          );
        });
      });
      relationIds.forEach(function (relationId) {
        Object.keys(normalized.relations[relationId]).forEach(function (key) {
          normalized.relations[relationId][key] = Boolean(
            candidate.relations && candidate.relations[relationId] && candidate.relations[relationId][key]
          );
        });
      });
      normalized.completed = Boolean(candidate.completed);
      normalized.results = Array.isArray(candidate.results) ? candidate.results.map(Boolean) : [];
      return normalized;
    }

    state.modelChallenges = Array.isArray(state.modelChallenges) ? state.modelChallenges : [];
    state.modelChallenges = config.challenges.map(function (_, index) {
      return normalizeChallengeState(state.modelChallenges[index]);
    });
    state.modelCurrent = Number.isInteger(state.modelCurrent) && config.challenges[state.modelCurrent]
      ? state.modelCurrent
      : 0;

    function currentState() {
      return state.modelChallenges[state.modelCurrent];
    }

    function hasModelActivity() {
      return state.modelChallenges.some(function (challengeState) {
        var hasPredicate = objectIds.some(function (objectId) {
          return predicateIds.some(function (predicateId) {
            return challengeState.assignments[objectId][predicateId];
          });
        });
        var hasRelation = relationIds.some(function (relationId) {
          return Object.values(challengeState.relations[relationId]).some(Boolean);
        });
        return hasPredicate || hasRelation || challengeState.results.length > 0;
      });
    }

    function evaluateCondition(condition, challengeState) {
      if (condition.kind === 'exists') {
        return objectIds.some(function (objectId) {
          var assignment = challengeState.assignments[objectId];
          return (condition.all || []).every(function (predicate) { return assignment[predicate]; }) &&
            (condition.none || []).every(function (predicate) { return !assignment[predicate]; });
        });
      }
      if (condition.kind === 'subset') {
        return objectIds.every(function (objectId) {
          var assignment = challengeState.assignments[objectId];
          return !assignment[condition.left] || assignment[condition.right];
        });
      }
      if (condition.kind === 'forall_exists_relation') {
        return objectIds.every(function (sourceId) {
          if (!challengeState.assignments[sourceId][condition.source_predicate]) {
            return true;
          }
          return objectIds.some(function (targetId) {
            return challengeState.assignments[targetId][condition.target_predicate] &&
              challengeState.relations[condition.relation][sourceId + ':' + targetId];
          });
        });
      }
      return false;
    }

    function renderConditions(challenge, challengeState) {
      conditionList.replaceChildren();
      challenge.conditions.forEach(function (condition, index) {
        var item = document.createElement('li');
        var result = challengeState.results[index];
        if (typeof result === 'boolean') {
          item.classList.add(result ? 'is-correct' : 'is-wrong');
        }
        var icon = document.createElement('i');
        icon.className = typeof result === 'boolean'
          ? 'bi ' + (result ? 'bi-check-circle-fill' : 'bi-x-circle-fill')
          : 'bi bi-circle';
        icon.setAttribute('aria-hidden', 'true');
        var label = document.createElement('span');
        label.textContent = condition.label;
        item.append(icon, label);
        conditionList.appendChild(item);
      });
    }

    function renderModel() {
      var challenge = config.challenges[state.modelCurrent];
      var challengeState = currentState();
      titleNode.textContent = challenge.title;
      promptNode.textContent = challenge.prompt;
      formulaNode.textContent = challenge.formula;
      relationPanel.hidden = !challenge.uses_relations;

      challengeButtons.forEach(function (button, index) {
        var selected = index === state.modelCurrent;
        button.setAttribute('aria-selected', selected ? 'true' : 'false');
        button.classList.toggle('is-active', selected);
        button.classList.toggle('is-complete', state.modelChallenges[index].completed);
      });

      predicateButtons.forEach(function (button) {
        var active = challengeState.assignments[button.dataset.objectId][button.dataset.modelPredicate];
        button.setAttribute('aria-pressed', active ? 'true' : 'false');
        button.classList.toggle('is-active', active);
      });

      lab.querySelectorAll('[data-model-object]').forEach(function (objectCard) {
        var assignment = challengeState.assignments[objectCard.dataset.modelObject];
        objectCard.classList.toggle('has-predicate', predicateIds.some(function (id) { return assignment[id]; }));
      });

      relationButtons.forEach(function (button) {
        var relationState = challengeState.relations[button.dataset.modelRelation];
        var active = relationState[button.dataset.sourceId + ':' + button.dataset.targetId];
        button.setAttribute('aria-pressed', active ? 'true' : 'false');
        button.classList.toggle('is-active', active);
        button.textContent = active ? '✓' : '-';
      });

      renderConditions(challenge, challengeState);
      var completedCount = state.modelChallenges.filter(function (item) { return item.completed; }).length;
      if (completedCount === config.challenges.length) {
        markLabComplete();
      } else if (completedCount) {
        setStatus(completedCount + '/' + config.challenges.length + ' görev tamamlandı', 'active');
      } else if (hasModelActivity()) {
        touchLab('Çalışma sürüyor');
      } else {
        setStatus('Başlamaya hazır');
      }
    }

    function invalidateCurrentResults() {
      currentState().results = [];
      clearFeedback(feedback);
      touchLab();
    }

    challengeButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        state.modelCurrent = Number(button.dataset.modelChallenge);
        clearFeedback(feedback);
        saveState();
        renderModel();
      });
    });

    predicateButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var assignment = currentState().assignments[button.dataset.objectId];
        assignment[button.dataset.modelPredicate] = !assignment[button.dataset.modelPredicate];
        invalidateCurrentResults();
        saveState();
        renderModel();
      });
    });

    relationButtons.forEach(function (button) {
      button.addEventListener('click', function () {
        var relationState = currentState().relations[button.dataset.modelRelation];
        var key = button.dataset.sourceId + ':' + button.dataset.targetId;
        relationState[key] = !relationState[key];
        invalidateCurrentResults();
        saveState();
        renderModel();
      });
    });

    checkButton.addEventListener('click', function () {
      var challenge = config.challenges[state.modelCurrent];
      var challengeState = currentState();
      challengeState.results = challenge.conditions.map(function (condition) {
        return evaluateCondition(condition, challengeState);
      });
      var passed = challengeState.results.every(Boolean);
      challengeState.completed = challengeState.completed || passed;
      if (passed) {
        setFeedback(feedback, 'Bu yapı formülü doğru yapan bir modeldir. Şimdi diğer göreve geçebilirsin.', 'success');
      } else {
        var correctCount = challengeState.results.filter(Boolean).length;
        setFeedback(feedback, correctCount + '/' + challenge.conditions.length + ' koşul sağlandı. Kırmızı koşulu karşılayacak atamayı değiştir.', 'warning');
      }
      saveState();
      renderModel();
    });

    resetButton.addEventListener('click', function () {
      var wasCompleted = currentState().completed;
      state.modelChallenges[state.modelCurrent] = blankChallengeState();
      state.modelChallenges[state.modelCurrent].completed = wasCompleted;
      clearFeedback(feedback);
      saveState();
      renderModel();
    });

    renderModel();
  }

  if (state.completed) {
    root.classList.add('is-complete');
    setStatus('Tamamlandı', 'complete');
  } else {
    setStatus('Başlamaya hazır');
  }

  if (config.type === 'truth_table') {
    initializeTruthTable(root.querySelector('[data-truth-table-lab]'));
  } else if (config.type === 'symbolization') {
    initializeSymbolization(root.querySelector('[data-symbolization-lab]'));
  } else if (config.type === 'proof_builder') {
    initializeProofBuilder(root.querySelector('[data-proof-builder]'));
  } else if (config.type === 'model_builder') {
    initializeModelBuilder(root.querySelector('[data-model-builder]'));
  }
})();
