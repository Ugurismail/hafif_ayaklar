/**
 * Shared left-frame navigation behavior.
 */

(function() {
    'use strict';

    const SHUFFLED_QUESTIONS_KEY = 'hafifayaklar:left-frame-shuffled-questions:v1';

    function notify(message, type) {
        if (typeof window.showToast === 'function') {
            window.showToast(message, type);
            return;
        }
        console.warn(message);
    }

    function normalizeQuestions(questions) {
        if (!Array.isArray(questions)) {
            return [];
        }

        return questions
            .filter(question => question && typeof question.slug === 'string' && typeof question.text === 'string')
            .slice(0, 20)
            .map(question => ({
                id: question.id,
                slug: question.slug,
                text: question.text,
                answers_count: Number.isFinite(Number(question.answers_count))
                    ? Number(question.answers_count)
                    : 0
            }));
    }

    function readStoredQuestions() {
        try {
            const stored = JSON.parse(window.sessionStorage.getItem(SHUFFLED_QUESTIONS_KEY));
            if (!stored) {
                return [];
            }
            return normalizeQuestions(stored.questions);
        } catch (error) {
            return [];
        }
    }

    function storeQuestions(questions) {
        try {
            window.sessionStorage.setItem(SHUFFLED_QUESTIONS_KEY, JSON.stringify({
                questions: questions
            }));
        } catch (error) {
            console.warn('Başlık listesi tarayıcı oturumunda saklanamadı.', error);
        }
    }

    function clearStoredQuestions() {
        try {
            window.sessionStorage.removeItem(SHUFFLED_QUESTIONS_KEY);
        } catch (error) {
            console.warn('Saklanan başlık listesi temizlenemedi.', error);
        }
    }

    function renderQuestions(questions) {
        const questionsList = document.getElementById('questions-list');
        if (!questionsList) {
            return false;
        }

        const fragment = document.createDocumentFragment();
        questions.forEach(function(question) {
            const li = document.createElement('li');
            li.className = 'tbas-color baslik left-question-row';

            const link = document.createElement('a');
            link.href = `/${encodeURIComponent(question.slug)}/`;
            link.className = 'tbas-color text-decoration-none left-question-link';

            const title = document.createElement('span');
            title.className = 'left-question-title';
            title.textContent = question.text;

            const count = document.createElement('small');
            count.className = 'left-question-count';
            count.textContent = String(question.answers_count);

            link.appendChild(title);
            link.appendChild(count);
            li.appendChild(link);
            fragment.appendChild(li);
        });

        questionsList.replaceChildren(fragment);
        return true;
    }

    function fetchQuestions() {
        return window.fetch('/shuffle_questions/', {
            headers: {'Accept': 'application/json'}
        }).then(function(response) {
            if (!response.ok) {
                throw new Error(`Başlık isteği ${response.status} durumuyla sonuçlandı.`);
            }
            return response.json();
        }).then(function(data) {
            return normalizeQuestions(data.questions);
        });
    }

    document.addEventListener('DOMContentLoaded', function() {
        const questionsList = document.getElementById('questions-list');
        const latestQuestionsMarkup = questionsList ? questionsList.innerHTML : '';
        const latestQuestionsBtn = document.getElementById('latest-questions-btn');
        const toolbar = document.querySelector('.left-navigation');
        if (!toolbar || !questionsList) return;
        const dayActive = toolbar.dataset.dayActive === 'true';
        const params = new URL(window.location.href).searchParams;
        const pagination = document.querySelector('[data-left-pagination]');
        const filtered = dayActive || params.has('followed');

        function setShuffledMode(active) {
            if (!latestQuestionsBtn) {
                return;
            }
            latestQuestionsBtn.hidden = !active;
            if (randomQuestionBtn) randomQuestionBtn.setAttribute('aria-pressed', String(active));
            if (pagination) pagination.hidden = active;
        }

        if (filtered || params.has('page') || params.has('q_page')) clearStoredQuestions();
        const randomQuestionBtn = document.getElementById('random-question-btn');
        const storedQuestions = readStoredQuestions();
        if (storedQuestions.length > 0) {
            setShuffledMode(renderQuestions(storedQuestions));
        }

        if (randomQuestionBtn) {
            randomQuestionBtn.addEventListener('click', function(event) {
                event.preventDefault();
                if (randomQuestionBtn.disabled) return;
                randomQuestionBtn.disabled = true;
                randomQuestionBtn.setAttribute('aria-busy', 'true');

                fetchQuestions()
                    .then(function(questions) {
                        if (questions.length === 0) {
                            notify('Gösterilecek başlık bulunamadı', 'warning');
                            return;
                        }
                        if (filtered) {
                            storeQuestions(questions);
                            const url = new URL(window.location.href);
                            ['day', 'followed', 'page', 'q_page'].forEach(key => url.searchParams.delete(key));
                            window.location.assign(url.toString());
                            return;
                        }
                        if (!renderQuestions(questions)) {
                            notify('Başlıkları listeleyecek alan bulunamadı', 'error');
                            return;
                        }
                        storeQuestions(questions);
                        setShuffledMode(true);
                    })
                    .catch(function(error) {
                        console.error('Shuffle error:', error);
                        notify('Başlıklar yüklenirken hata oluştu', 'error');
                    })
                    .finally(function() {
                        randomQuestionBtn.removeAttribute('aria-busy');
                        randomQuestionBtn.disabled = false;
                    });
            });
        }

        if (latestQuestionsBtn) {
            latestQuestionsBtn.addEventListener('click', function(event) {
                clearStoredQuestions();
                if (dayActive) return;
                event.preventDefault();
                if (questionsList) {
                    questionsList.innerHTML = latestQuestionsMarkup;
                }
                setShuffledMode(false);
            });
        }

        const dateForm = toolbar.querySelector('.left-date-form');
        const dateToggle = document.getElementById('left-date-toggle');
        if (dateForm && dateToggle) {
            dateToggle.addEventListener('click', function() {
                dateForm.hidden = !dateForm.hidden;
                dateToggle.setAttribute('aria-expanded', String(!dateForm.hidden));
                if (!dateForm.hidden) document.getElementById('left-day-input').focus();
            });
            dateForm.addEventListener('keydown', function(event) {
                if (event.key === 'Escape') {
                    dateForm.hidden = true;
                    dateToggle.setAttribute('aria-expanded', 'false');
                    dateToggle.focus();
                }
            });
        }
        if (dateForm) dateForm.addEventListener('submit', clearStoredQuestions);
        const followForm = document.getElementById('left-follow-form');
        if (followForm) followForm.addEventListener('change', function() {
            clearStoredQuestions();
            followForm.requestSubmit();
        });
        const allLink = toolbar.querySelector('[data-left-all]');
        if (allLink) allLink.addEventListener('click', clearStoredQuestions);

        const shuffleBtn = document.getElementById('shuffle-btn');
        if (shuffleBtn) {
            shuffleBtn.addEventListener('click', function(event) {
                event.preventDefault();
                fetchQuestions()
                    .then(function(questions) {
                        if (questions.length > 0) {
                            const question = questions[Math.floor(Math.random() * questions.length)];
                            window.location.href = `/${encodeURIComponent(question.slug)}/`;
                        }
                    })
                    .catch(function(error) {
                        console.error('Shuffle error:', error);
                        notify('Başlık yüklenirken hata oluştu', 'error');
                    });
            });
        }
    });
})();
