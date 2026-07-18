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
            li.className = 'tbas-color baslik d-flex justify-content-between align-items-center mt-2';

            const link = document.createElement('a');
            link.href = `/${encodeURIComponent(question.slug)}/`;
            link.className = 'tbas-color text-decoration-none d-flex justify-content-between align-items-center w-100';

            const title = document.createElement('span');
            title.textContent = question.text;

            const count = document.createElement('small');
            count.className = 'text-muted ms-2';
            count.style.minWidth = '20px';
            count.style.textAlign = 'right';
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

        function setShuffledMode(active) {
            if (!latestQuestionsBtn) {
                return;
            }
            latestQuestionsBtn.hidden = !active;
            latestQuestionsBtn.classList.toggle('d-none', !active);
        }

        const storedQuestions = readStoredQuestions();
        if (storedQuestions.length > 0) {
            setShuffledMode(renderQuestions(storedQuestions));
        }

        const randomQuestionBtn = document.getElementById('random-question-btn');
        if (randomQuestionBtn) {
            randomQuestionBtn.addEventListener('click', function(event) {
                event.preventDefault();
                randomQuestionBtn.setAttribute('aria-busy', 'true');

                fetchQuestions()
                    .then(function(questions) {
                        if (questions.length === 0) {
                            notify('Gösterilecek başlık bulunamadı', 'warning');
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
                    });
            });
        }

        if (latestQuestionsBtn) {
            latestQuestionsBtn.addEventListener('click', function(event) {
                event.preventDefault();
                clearStoredQuestions();
                if (questionsList) {
                    questionsList.innerHTML = latestQuestionsMarkup;
                }
                setShuffledMode(false);
            });
        }

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
