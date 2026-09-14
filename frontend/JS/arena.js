/* AlgoQuest - Arena Page JavaScript */

document.addEventListener('DOMContentLoaded', () => {
  const enterDuelBtn = document.getElementById('enter-duel-btn');
  const arenaIntro = document.getElementById('arena-intro');
  const battleContainer = document.getElementById('battle-container');
  const timerDisplay = document.getElementById('timer-display');
  const optionCards = document.querySelectorAll('.option-card');
  const proceedBtn = document.getElementById('proceed-btn');

  let timerInterval = null;
  let seconds = 2;

  if (enterDuelBtn && arenaIntro && battleContainer) {
    enterDuelBtn.addEventListener('click', () => {
      arenaIntro.style.display = 'none';
      battleContainer.style.display = 'block';
      startTimer();
    });
  }

  function startTimer() {
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(() => {
      seconds++;
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      if (timerDisplay) {
        timerDisplay.textContent = `⏱️ ${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      }
    }, 1000);
  }

  optionCards.forEach(card => {
    card.addEventListener('click', () => {
      optionCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
    });
  });

  if (proceedBtn) {
    proceedBtn.addEventListener('click', () => {
      alert('Proceeding to Battle Phase 2: State Prediction!');
    });
  }
});
