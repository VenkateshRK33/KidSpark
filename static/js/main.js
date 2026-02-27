/* ══════════════════════════════════════
   KIDSPARK — MAIN JS
   Handles: ripple, cursor trail, badge toast,
   XP float, quiz logic, avatar selection,
   puzzle hover, stage navigation, confetti
══════════════════════════════════════ */

/* ── Ripple effect on all buttons ── */
function initRipple() {
  document.querySelectorAll('.btn, .btn-logout, .btn-mission, .btn-resume, .btn-hero, .q-ans, .scenario-choice, .chat-choice-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      ripple.style.cssText = `
        position:absolute;border-radius:50%;
        background:rgba(255,255,255,0.32);
        width:8px;height:8px;
        left:${e.clientX - rect.left - 4}px;
        top:${e.clientY - rect.top - 4}px;
        transform:scale(0);
        animation:ripple 0.6s ease forwards;
        pointer-events:none;z-index:10;
      `;
      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);
      setTimeout(() => ripple.remove(), 700);
    });
  });
}

/* ── Puzzle letter bouncy hover ── */
function initPuzzleHover() {
  document.querySelectorAll('.pl').forEach(pl => {
    pl.addEventListener('mouseenter', () => {
      const deg = Math.random() * 14 - 7;
      pl.style.transform = `translateY(-8px) scale(1.28) rotate(${deg}deg)`;
    });
    pl.addEventListener('mouseleave', () => {
      pl.style.transform = '';
    });
  });
}

/* ── Avatar card selection ── */
function initAvatarSelection() {
  const cards = document.querySelectorAll('.av-card');
  const input = document.querySelector('input[name="avatar"]');
  const submitBtn = document.querySelector('.av-submit-btn');
  if (!cards.length) return;
  if (submitBtn) submitBtn.disabled = true;
  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      if (input) input.value = card.dataset.value;
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('btn-disabled');
      }
    });
  });
}

/* ── Badge toast notification ── */
function showBadgeToast(name, icon) {
  const toast = document.getElementById('badgeToast');
  const toastIcon = document.getElementById('toastIcon');
  const toastName = document.getElementById('toastName');
  if (!toast) return;
  if (toastIcon) toastIcon.textContent = icon || '🏆';
  if (toastName) toastName.textContent = name || 'Badge Earned!';
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 4000);
}

/* ── XP float animation ── */
function spawnXPFloat(x, y, text) {
  const container = document.getElementById('xpFloatContainer');
  if (!container) return;
  const floater = document.createElement('div');
  floater.className = 'xp-float';
  floater.textContent = text || '+10 XP ⭐';
  floater.style.left = (x || window.innerWidth / 2) + 'px';
  floater.style.top  = (y || window.innerHeight / 2) + 'px';
  container.appendChild(floater);
  setTimeout(() => floater.remove(), 1600);
}

/* ── Count up animation ── */
function countUp(el, target, duration) {
  duration = duration || 900;
  let start = 0;
  const step = target / (duration / 16);
  const timer = setInterval(() => {
    start = Math.min(start + step, target);
    el.textContent = Math.round(start);
    if (start >= target) clearInterval(timer);
  }, 16);
}

/* ── Confetti burst (result page) ── */
function fireResultConfetti() {
  if (typeof confetti === 'undefined') return;
  confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 } });
  setTimeout(() => confetti({ particleCount: 80, angle: 60,  spread: 55, origin: { x: 0 } }), 500);
  setTimeout(() => confetti({ particleCount: 80, angle: 120, spread: 55, origin: { x: 1 } }), 900);
  setTimeout(() => {
    const end = Date.now() + 1800;
    (function frame() {
      confetti({ particleCount: 3, angle: 60,  spread: 55, origin: { x: 0 }, colors: ['#fbbf24','#f43f5e','#6366f1'] });
      confetti({ particleCount: 3, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#fbbf24','#f43f5e','#6366f1'] });
      if (Date.now() < end) requestAnimationFrame(frame);
    })();
  }, 1400);
}

/* ── Cinematic result overlay ── */
function initResultReveal() {
  const overlay = document.getElementById('resultOverlay');
  if (!overlay) return;
  overlay.style.animation = 'overlayFadeOut 1.8s ease 0.5s forwards';
  setTimeout(() => {
    overlay.remove();
    fireResultConfetti();
    animateResultRings();
  }, 2200);
}

/* ── Animate SVG result rings ── */
function animateResultRings() {
  document.querySelectorAll('.ring-fill[data-pct]').forEach((ring, i) => {
    const pct = parseFloat(ring.dataset.pct);
    const circumference = 251;
    const offset = circumference - (pct / 100) * circumference;
    setTimeout(() => {
      ring.style.strokeDashoffset = offset;
    }, i * 200);
  });
  document.querySelectorAll('.ring-pct[data-count]').forEach(el => {
    countUp(el, parseInt(el.dataset.count));
  });
}

/* ── Animate progress bar fills ── */
function animateBars() {
  document.querySelectorAll('.prog-fill[data-width]').forEach(bar => {
    const w = bar.dataset.width;
    setTimeout(() => { bar.style.width = w + '%'; }, 200);
  });
  document.querySelectorAll('.hc-bar-fill[data-width]').forEach(bar => {
    const w = bar.dataset.width;
    setTimeout(() => { bar.style.width = w + '%'; }, 300);
  });
}

/* ── Stage 2 scenario navigation ── */
function initScenarioNav() {
  let current = 0;
  const slides = document.querySelectorAll('.scenario-slide');
  const counter = document.getElementById('scenarioCounter');
  const form = document.getElementById('stage2Form');
  const collected = {};
  if (!slides.length) return;
  
  function showSlide(idx) {
    slides.forEach((s, i) => {
      if (i === idx) {
        s.style.display = 'block';
        s.style.animation = 'slideInRight2 0.4s cubic-bezier(0.34,1.56,0.64,1)';
      } else {
        s.style.display = 'none';
      }
    });
    if (counter) counter.textContent = `${idx + 1} / ${slides.length}`;
  }
  
  document.querySelectorAll('.scenario-choice').forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('.scenario-slide');
      parent.querySelectorAll('.scenario-choice').forEach(b => b.classList.remove('chosen'));
      btn.classList.add('chosen');
      const field = btn.dataset.field;
      const val   = btn.dataset.value;
      collected[field] = val;
      let inp = form ? form.querySelector(`input[name="${field}"]`) : null;
      if (!inp && form) {
        inp = document.createElement('input');
        inp.type = 'hidden'; inp.name = field;
        form.appendChild(inp);
      }
      if (inp) inp.value = val;
      setTimeout(() => {
        if (current < slides.length - 1) {
          current++;
          showSlide(current);
        } else if (form) {
          form.submit();
        }
      }, 350);
    });
  });
  showSlide(0);
}

/* ── Stage 3 tap grid + timer ── */
function initTapGrid(duration) {
  const timerEl = document.getElementById('timerDisplay');
  const form    = document.getElementById('stage3Form');
  const tapped  = new Set();
  let remaining = duration || 30;
  
  document.querySelectorAll('.tap-card').forEach(card => {
    card.addEventListener('click', () => {
      const val = card.dataset.hobby;
      if (tapped.has(val)) {
        tapped.delete(val);
        card.classList.remove('tapped');
      } else {
        tapped.add(val);
        card.classList.add('tapped');
        const rect = card.getBoundingClientRect();
        spawnXPFloat(rect.left + rect.width / 2, rect.top, '⭐');
      }
      updateTappedInput();
    });
  });
  
  function updateTappedInput() {
    if (!form) return;
    let inp = form.querySelector('input[name="tapped_items"]');
    if (!inp) {
      inp = document.createElement('input');
      inp.type = 'hidden'; inp.name = 'tapped_items';
      form.appendChild(inp);
    }
    inp.value = [...tapped].join(',');
  }
  
  const interval = setInterval(() => {
    remaining--;
    if (timerEl) {
      timerEl.textContent = remaining;
      if (remaining <= 10) timerEl.classList.add('urgent');
    }
    if (remaining <= 0) {
      clearInterval(interval);
      updateTappedInput();
      if (form) form.submit();
    }
  }, 1000);
}

/* ── Stage 5 chat navigation ── */
function initChatNav() {
  const bubbles = document.querySelectorAll('.chat-bubble-item');
  let current = 0;
  if (!bubbles.length) return;
  
  function showBubble(idx) {
    const bubble = bubbles[idx];
    if (!bubble) return;
    bubble.style.display = 'block';
    bubble.style.animation = 'chatAppear 0.4s cubic-bezier(0.34,1.56,0.64,1)';
  }
  
  document.querySelectorAll('.chat-choice-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const parent = btn.closest('.chat-choices');
      parent.querySelectorAll('.chat-choice-btn').forEach(b => b.classList.remove('chosen'));
      btn.classList.add('chosen');
      parent.querySelectorAll('.chat-choice-btn').forEach(b => b.disabled = true);
      const field = btn.dataset.field;
      const val   = btn.dataset.value;
      const form  = document.getElementById('stage5Form');
      if (form) {
        let inp = form.querySelector(`input[name="${field}"]`);
        if (!inp) {
          inp = document.createElement('input');
          inp.type = 'hidden'; inp.name = field;
          form.appendChild(inp);
        }
        inp.value = val;
      }
      setTimeout(() => {
        current++;
        if (current < bubbles.length) {
          showBubble(current);
        } else if (form) {
          form.submit();
        }
      }, 400);
    });
  });
  
  bubbles.forEach((b, i) => {
    b.style.display = i === 0 ? 'block' : 'none';
  });
}

/* ── Quiz interactions ── */
function initQuiz() {
  const blocks = document.querySelectorAll('.question-block');
  if (!blocks.length) return;
  let current = 0;
  let answered = false;
  const answers = [];
  
  function showBlock(idx) {
    blocks.forEach((b, i) => b.style.display = i === idx ? 'block' : 'none');
    document.querySelectorAll('.q-dot').forEach((d, i) => {
      d.classList.toggle('active', i === idx);
      d.classList.toggle('done',   i < idx);
    });
    answered = false;
  }
  
  document.querySelectorAll('.q-ans').forEach(btn => {
    btn.addEventListener('click', function() {
      if (answered) return;
      answered = true;
      const isCorrect = this.dataset.correct === 'true';
      const block = this.closest('.question-block');
      block.querySelectorAll('.q-ans').forEach(b => b.style.pointerEvents = 'none');
      this.classList.add(isCorrect ? 'correct' : 'wrong');
      if (!isCorrect) {
        block.querySelectorAll('.q-ans').forEach(b => {
          if (b.dataset.correct === 'true') b.classList.add('correct');
        });
      } else {
        if (typeof confetti !== 'undefined') {
          const rect = this.getBoundingClientRect();
          confetti({ particleCount: 30, spread: 50, origin: { x: rect.left / window.innerWidth, y: rect.top / window.innerHeight }, scalar: 0.6 });
        }
      }
      const exp = block.querySelector('.explanation-box');
      if (exp) exp.classList.add('show');
      answers.push({ opt: this.dataset.option, correct: isCorrect });
      const nextBtn = block.querySelector('.next-q-btn');
      if (nextBtn) nextBtn.style.display = 'inline-flex';
    });
  });
  
  document.querySelectorAll('.next-q-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      current++;
      if (current < blocks.length) {
        showBlock(current);
      } else {
        const form = document.getElementById('quizSubmitForm');
        if (form) {
          answers.forEach(a => {
            const inp = document.createElement('input');
            inp.type = 'hidden'; inp.name = 'answer'; inp.value = a.opt;
            form.appendChild(inp);
          });
          form.submit();
        }
      }
    });
  });
  
  showBlock(0);
}

/* ── Daily challenge submit with fireworks ── */
function initChallengeSubmit() {
  const form = document.querySelector('#challengeForm');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    const btn = form.querySelector('button[type=submit]');
    if (btn) {
      btn.textContent = '🎉 Submitting...';
      btn.disabled = true;
    }
    if (typeof confetti !== 'undefined') {
      confetti({ particleCount: 80, spread: 90, origin: { y: 0.8 }, colors: ['#fbbf24','#f43f5e','#6366f1'] });
    }
    const rect = btn ? btn.getBoundingClientRect() : null;
    if (rect) spawnXPFloat(rect.left + rect.width / 2, rect.top, '+20 XP ⭐');
  });
}

/* ── Auto dismiss flash messages ── */
function initFlashMessages() {
  document.querySelectorAll('.flash').forEach(flash => {
    setTimeout(() => {
      flash.style.animation = 'slideOutRight 0.4s ease forwards';
      setTimeout(() => flash.remove(), 450);
    }, 4000);
  });
}

/* ── Count up all nav stats and streak numbers ── */
function initCountUps() {
  document.querySelectorAll('[data-count-up]').forEach(el => {
    const target = parseInt(el.dataset.countUp);
    if (!isNaN(target)) countUp(el, target);
  });
}

/* ══════════════════════════════════════
   INIT ON DOM READY
══════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  initRipple();
  initPuzzleHover();
  initAvatarSelection();
  initFlashMessages();
  initCountUps();
  animateBars();
  
  /* page-specific inits */
  if (document.getElementById('resultOverlay'))   initResultReveal();
  if (document.getElementById('resultPage'))      { fireResultConfetti(); animateResultRings(); }
  if (document.querySelector('.question-block'))  initQuiz();
  if (document.querySelector('.scenario-slide'))  initScenarioNav();
  if (document.querySelector('.tap-card'))        initTapGrid(parseInt(document.getElementById('tapTimer')?.dataset.duration || '30'));
  if (document.querySelector('.chat-bubble-item')) initChatNav();
  if (document.getElementById('challengeForm'))   initChallengeSubmit();
});
