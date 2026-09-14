/* AlgoQuest - Thinking Trial JavaScript */

document.addEventListener('DOMContentLoaded', () => {
  const trialOptions = document.querySelectorAll('.trial-option-item');
  const verifyBtn = document.getElementById('verify-btn');

  trialOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      trialOptions.forEach(o => o.classList.remove('selected'));
      opt.classList.add('selected');
    });
  });

  if (verifyBtn) {
    verifyBtn.addEventListener('click', () => {
      const selected = document.querySelector('.trial-option-item.selected');
      if (!selected) {
        alert('Please select an answer option first!');
        return;
      }

      if (selected.textContent.includes('maximum score and the minimum score')) {
        alert('Correct! You correctly identified that finding the difference requires tracking both the maximum score and minimum score. Moving to Step 2/5 (Identify Invariant)...');
        window.location.href = 'adventure.html';
      } else {
        alert('Incorrect answer. Hint: To calculate difference, you need the highest value and the lowest value.');
      }
    });
  }
});
