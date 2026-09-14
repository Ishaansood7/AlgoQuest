/* AlgoQuest - Profile Page JavaScript */

document.addEventListener('DOMContentLoaded', () => {
  const langBtns = document.querySelectorAll('.lang-btn');
  const resetBtn = document.getElementById('reset-demo-btn');

  langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      langBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    });
  });

  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      const confirmReset = confirm('Are you sure you want to reset all user stats, badges, and learning progress to initial demo state?');
      if (confirmReset) {
        alert('Progress reset successfully to initial demo state!');
      }
    });
  }
});
