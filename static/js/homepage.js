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
                    const li = document.createElement('li');
                    li.className = 'tbas-color baslik d-flex justify-content-between align-items-center mt-2';

                    const a = document.createElement('a');
                    a.href = link;
                    a.className = 'tbas-color text-decoration-none d-flex justify-content-between align-items-center w-100';

                    const title = document.createElement('span');
                    title.textContent = q.text;

                    const count = document.createElement('small');
                    count.className = 'text-muted ms-2';
                    count.style.minWidth = '20px';
                    count.style.textAlign = 'right';
                    count.textContent = String(q.answers_count);

                    a.appendChild(title);
                    a.appendChild(count);
                    li.appendChild(a);
                    questionsList.appendChild(li);
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
