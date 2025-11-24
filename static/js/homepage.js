/**
 * Homepage specific JavaScript
 * Handles random question shuffling and navigation
 */

document.addEventListener('DOMContentLoaded', function() {
    // Shuffle butonu (sol frame'i random doldurur)
    const randomQuestionBtn = document.getElementById('random-question-btn');
    if (randomQuestionBtn) {
        randomQuestionBtn.addEventListener('click', function(e) {
            e.preventDefault();
            fetch('/shuffle_questions/')
            .then(response => response.json())
            .then(data => {
                const questionsList = document.getElementById('questions-list');
                if (!questionsList) {
                    showToast('Soruları listeleyecek alan bulunamadı!', 'error');
                    return;
                }
                questionsList.innerHTML = '';
                data.questions.forEach(function(q) {
                    const link = `/${q.slug}/`;
                    questionsList.innerHTML += `
                        <li class="tbas-color baslik d-flex justify-content-between align-items-center mt-2">
                            <a href="${link}" class="tbas-color text-decoration-none d-flex justify-content-between align-items-center w-100">
                                <span>${q.text}</span>
                                <small class="text-muted ms-2" style="min-width: 20px; text-align: right;">${q.answers_count}</small>
                            </a>
                        </li>
                    `;
                });
            })
            .catch(error => {
                console.error('Shuffle error:', error);
                showToast('Başlıklar yüklenirken hata oluştu', 'error');
            });
        });
    }

    // Rastgele başlığa git butonu
    const shuffleBtn = document.getElementById('shuffle-btn');
    if (shuffleBtn) {
        shuffleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            fetch('/shuffle_questions/')
            .then(response => response.json())
            .then(data => {
                if (data.questions && data.questions.length > 0) {
                    const q = data.questions[Math.floor(Math.random() * data.questions.length)];
                    const link = `/${q.slug}/`;
                    window.location.href = link;
                }
            })
            .catch(error => {
                console.error('Shuffle error:', error);
                showToast('Başlık yüklenirken hata oluştu', 'error');
            });
        });
    }
});
