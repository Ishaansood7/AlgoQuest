/* AlgoQuest - Main JavaScript (Global Interactivity, Theme Switcher & AlgoBot AI Coach Modal) */

document.addEventListener('DOMContentLoaded', () => {
  // Theme Toggle Switcher Logic (Day / Light Mode vs Night / Dark Mode)
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  
  // Load saved theme preference from localStorage
  const savedTheme = localStorage.getItem('algoquest_theme') || 'dark';
  if (savedTheme === 'light') {
    document.body.classList.add('light-mode');
    if (themeToggleBtn) {
      themeToggleBtn.innerHTML = '☀️ Light';
    }
  } else {
    document.body.classList.remove('light-mode');
    if (themeToggleBtn) {
      themeToggleBtn.innerHTML = '🌙 Dark';
    }
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('light-mode');
      const isLight = document.body.classList.contains('light-mode');
      localStorage.setItem('algoquest_theme', isLight ? 'light' : 'dark');
      themeToggleBtn.innerHTML = isLight ? '☀️ Light' : '🌙 Dark';
    });
  }

  // Highlight active navigation tab based on current path
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    if (href === currentPath || (currentPath === '' && href === 'index.html')) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // Mobile Menu Hamburger Toggle
  const mobileToggle = document.getElementById('mobile-menu-toggle');
  const navCenter = document.querySelector('.nav-center');

  if (mobileToggle && navCenter) {
    mobileToggle.addEventListener('click', () => {
      navCenter.classList.toggle('open');
      mobileToggle.textContent = navCenter.classList.contains('open') ? '✕' : '☰';
    });
  }

  // AlgoBot AI Coach Modal Interactivity
  const algobotBtn = document.getElementById('algobot-btn');
  const algobotModal = document.getElementById('algobot-modal');
  const closeAlgobotBtn = document.getElementById('close-algobot');

  if (algobotBtn && algobotModal) {
    algobotBtn.addEventListener('click', () => {
      algobotModal.classList.add('active');
    });
  }

  if (closeAlgobotBtn && algobotModal) {
    closeAlgobotBtn.addEventListener('click', () => {
      algobotModal.classList.remove('active');
    });
  }

  // Close modal when clicking on overlay background
  if (algobotModal) {
    algobotModal.addEventListener('click', (e) => {
      if (e.target === algobotModal) {
        algobotModal.classList.remove('active');
      }
    });
  }

  // Quick Action Buttons inside AlgoBot
  const quickBtns = document.querySelectorAll('.quick-btn');
  const chatBody = document.querySelector('.algobot-chat-body');

  quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const actionText = btn.textContent.trim();
      appendChatMessage('user', actionText);

      setTimeout(() => {
        let botResponse = "Let's examine the invariants for this state. What variables need to remain stable during traversal?";
        if (actionText.includes('Nudge')) {
          botResponse = "Hint Level 1: Focus on the bounds of the array. What index represents the start, and what index is the end?";
        } else if (actionText.includes('Diagnose')) {
          botResponse = "Diagnostic check: Your pointer logic looks solid, but remember to verify empty array edge cases!";
        } else if (actionText.includes('Invariant')) {
          botResponse = "Loop Invariant: At iteration i, subarray [0..i-1] contains all evaluated elements with max frequency saved.";
        }
        appendChatMessage('algobot', botResponse);
      }, 500);
    });
  });

  // Chat Input Submission
  const chatInput = document.getElementById('chat-input');
  const sendBtn = document.getElementById('send-chat-btn');

  function handleSend() {
    if (!chatInput) return;
    const text = chatInput.value.trim();
    if (text.length === 0) return;

    appendChatMessage('user', text);
    chatInput.value = '';

    setTimeout(() => {
      appendChatMessage('algobot', `Great question! To think through "${text}", break down what information must survive across each loop step.`);
    }, 600);
  }

  if (sendBtn) sendBtn.addEventListener('click', handleSend);
  if (chatInput) {
    chatInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') handleSend();
    });
  }

  function appendChatMessage(sender, text) {
    if (!chatBody) return;
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    if (sender === 'user') {
      bubble.style.background = 'rgba(2, 132, 199, 0.15)';
      bubble.style.borderColor = 'rgba(2, 132, 199, 0.3)';
      bubble.style.alignSelf = 'flex-end';
      bubble.style.color = 'var(--text-main)';
    }
    
    const p = document.createElement('p');
    p.textContent = text;
    
    const time = document.createElement('div');
    time.className = 'chat-timestamp';
    time.textContent = sender === 'user' ? 'You • Just now' : 'AlgoBot • Just now';
    
    bubble.appendChild(p);
    bubble.appendChild(time);
    chatBody.appendChild(bubble);
    chatBody.scrollTop = chatBody.scrollHeight;
  }
});
