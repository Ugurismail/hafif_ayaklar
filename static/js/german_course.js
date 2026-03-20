document.addEventListener('DOMContentLoaded', function () {
    if (typeof bootstrap !== 'undefined') {
        Array.from(document.querySelectorAll('.reading-gloss-term[data-bs-toggle="tooltip"]')).forEach(function (el) {
            bootstrap.Tooltip.getOrCreateInstance(el, {
                trigger: 'hover focus click',
                container: 'body'
            });
        });
    }

    var exerciseCards = Array.from(document.querySelectorAll('.exercise-card'));
    if (!exerciseCards.length) {
        return;
    }

    var progressBars = Array.from(document.querySelectorAll('[data-german-progress-bar]'));
    var summaryTargets = {
        correct: Array.from(document.querySelectorAll('[data-german-summary="correct"]')),
        total: Array.from(document.querySelectorAll('[data-german-summary="total"]')),
        completed: Array.from(document.querySelectorAll('[data-german-summary="completed"]')),
        success: Array.from(document.querySelectorAll('[data-german-summary="success"]')),
        status: Array.from(document.querySelectorAll('[data-german-summary="status"]'))
    };
    var resetButtons = Array.from(document.querySelectorAll('[data-role="reset-lesson"]'));
    var passContainer = document.querySelector('[data-german-pass-correct]');
    var passCorrect = passContainer ? parseInt(passContainer.dataset.germanPassCorrect || '', 10) : NaN;
    var passTotal = passContainer ? parseInt(passContainer.dataset.germanPassTotal || '', 10) : NaN;

    function setText(targets, value) {
        targets.forEach(function (target) {
            target.textContent = value;
        });
    }

    function getLessonState() {
        var totalQuestions = 0;
        var totalCorrect = 0;
        var completedModules = 0;

        exerciseCards.forEach(function (card) {
            var questions = Array.from(card.querySelectorAll('.exercise-question'));
            var moduleComplete = questions.length > 0;

            totalQuestions += questions.length;

            questions.forEach(function (question) {
                var selected = question.querySelector('input[type="radio"]:checked');
                if (!selected) {
                    moduleComplete = false;
                    return;
                }

                if (selected.value === question.dataset.correctIndex) {
                    totalCorrect += 1;
                }
            });

            if (moduleComplete) {
                completedModules += 1;
            }
        });

        return {
            totalQuestions: totalQuestions,
            totalCorrect: totalCorrect,
            completedModules: completedModules,
            successRate: totalQuestions ? Math.round((totalCorrect / totalQuestions) * 100) : 0
        };
    }

    function updateSummary() {
        var state = getLessonState();

        setText(summaryTargets.correct, String(state.totalCorrect));
        setText(summaryTargets.total, String(state.totalQuestions));
        setText(summaryTargets.completed, String(state.completedModules));
        setText(summaryTargets.success, '%' + String(state.successRate));

        if (summaryTargets.status.length && !Number.isNaN(passCorrect)) {
            var statusText = 'Baraj: ' + String(passCorrect) + '/' + String(Number.isNaN(passTotal) ? state.totalQuestions : passTotal);
            if (state.completedModules === exerciseCards.length && state.totalQuestions > 0) {
                statusText = state.totalCorrect >= passCorrect ? 'Geçti' : 'Kaldı';
            }
            setText(summaryTargets.status, statusText);
        }

        progressBars.forEach(function (bar) {
            bar.style.width = state.successRate + '%';
        });
    }

    exerciseCards.forEach(function (card) {
        var checkButton = card.querySelector('[data-role="check-exercise"]');
        var summary = card.querySelector('[data-role="exercise-summary"]');

        if (!checkButton) {
            return;
        }

        checkButton.addEventListener('click', function () {
            var questions = Array.from(card.querySelectorAll('.exercise-question'));
            var correctAnswers = 0;
            var unanswered = 0;

            questions.forEach(function (question) {
                var options = Array.from(question.querySelectorAll('.exercise-option'));
                var feedback = question.querySelector('.question-feedback');
                var selected = question.querySelector('input[type="radio"]:checked');

                options.forEach(function (option) {
                    option.classList.remove('correct');
                    option.classList.remove('wrong');
                });

                if (!selected) {
                    unanswered += 1;
                    if (feedback) {
                        feedback.textContent = 'Bu soruyu boş bıraktın.';
                    }
                    return;
                }

                var selectedOption = selected.closest('.exercise-option');
                if (selected.value === question.dataset.correctIndex) {
                    correctAnswers += 1;
                    if (selectedOption) {
                        selectedOption.classList.add('correct');
                    }
                    if (feedback) {
                        feedback.textContent = 'Doğru. ' + feedback.dataset.explanation;
                    }
                } else {
                    if (selectedOption) {
                        selectedOption.classList.add('wrong');
                    }

                    var correctOption = question.querySelector('input[value="' + question.dataset.correctIndex + '"]');
                    if (correctOption && correctOption.closest('.exercise-option')) {
                        correctOption.closest('.exercise-option').classList.add('correct');
                    }

                    if (feedback) {
                        feedback.textContent = 'Yanlış. ' + feedback.dataset.explanation;
                    }
                }
            });

            if (summary) {
                summary.textContent = correctAnswers + '/' + questions.length + ' doğru';
                if (unanswered > 0) {
                    summary.textContent += ' | ' + unanswered + ' soru boş';
                }
            }

            if (unanswered > 0) {
                showToast('Bazı sorular boş kaldı. Yine de mevcut seçimlerin kontrol edildi.', 'warning');
            } else if (correctAnswers === questions.length) {
                showToast('Bu modülü temiz geçtin.', 'success');
            } else {
                showToast('Modül kontrol edildi. Açıklamaları oku ve tekrar dene.', 'info');
            }

            updateSummary();
        });
    });

    resetButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            exerciseCards.forEach(function (card) {
                Array.from(card.querySelectorAll('input[type="radio"]')).forEach(function (input) {
                    input.checked = false;
                });

                Array.from(card.querySelectorAll('.exercise-option')).forEach(function (option) {
                    option.classList.remove('correct');
                    option.classList.remove('wrong');
                });

                Array.from(card.querySelectorAll('.question-feedback')).forEach(function (feedback) {
                    feedback.textContent = '';
                });
            });

            updateSummary();
            showToast('Ders sıfırlandı. Soruları yeniden çözmeye hazırsın.', 'info');
        });
    });

    updateSummary();
});
