// Dashboard JavaScript - Tab switching, animations, and interactions

// Tab switching for parent dashboard
function switchTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(tabName + '-tab');
    if (selectedTab) {
        selectedTab.classList.add('active');
    }
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Badge popup notification
function showBadgePopup(badgeName, badgeIcon) {
    const popup = document.createElement('div');
    popup.className = 'badge-popup-notification';
    popup.innerHTML = `
        <div class="badge-popup-content">
            <div class="badge-popup-icon">${badgeIcon}</div>
            <div class="badge-popup-title">🏆 New Badge Earned!</div>
            <div class="badge-popup-name">${badgeName}</div>
        </div>
    `;
    
    document.body.appendChild(popup);
    
    // Trigger animation
    setTimeout(() => {
        popup.classList.add('show');
    }, 100);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        popup.classList.remove('show');
        setTimeout(() => {
            popup.remove();
        }, 300);
    }, 3000);
}

// Confetti animation for badge earning
function triggerConfetti() {
    if (typeof confetti !== 'undefined') {
        confetti({
            particleCount: 100,
            spread: 70,
            origin: { y: 0.6 }
        });
    }
}

// Check for newly earned badges on page load
document.addEventListener('DOMContentLoaded', function() {
    // Check if there are newly earned badges in session
    const newlyEarnedBadges = document.querySelector('[data-newly-earned]');
    if (newlyEarnedBadges) {
        const badges = JSON.parse(newlyEarnedBadges.dataset.newlyEarned || '[]');
        if (badges.length > 0) {
            // Trigger confetti
            triggerConfetti();
            
            // Show popup for each badge (with delay)
            badges.forEach((badge, index) => {
                setTimeout(() => {
                    showBadgePopup(badge.name, badge.icon);
                }, index * 3500);
            });
        }
    }
    
    // Animate progress bars on load
    const progressBars = document.querySelectorAll('.progress-fill, .hobby-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.width = width;
        }, 100);
    });
    
    // Animate stat numbers
    const statNumbers = document.querySelectorAll('.stat-number, .xp-number, .streak-number');
    statNumbers.forEach(stat => {
        const target = parseInt(stat.textContent);
        if (!isNaN(target)) {
            animateNumber(stat, 0, target, 1000);
        }
    });
});

// Animate number counting up
function animateNumber(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// Add CSS for badge popup if not already present
if (!document.getElementById('badge-popup-styles')) {
    const style = document.createElement('style');
    style.id = 'badge-popup-styles';
    style.textContent = `
        .badge-popup-notification {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) scale(0);
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            z-index: 10000;
            text-align: center;
            transition: transform 0.3s ease;
        }
        
        .badge-popup-notification.show {
            transform: translate(-50%, -50%) scale(1);
        }
        
        .badge-popup-icon {
            font-size: 80px;
            margin-bottom: 20px;
            animation: bounce 0.5s ease;
        }
        
        .badge-popup-title {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .badge-popup-name {
            font-size: 20px;
            color: #333;
        }
        
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-20px); }
        }
    `;
    document.head.appendChild(style);
}

// Export functions for use in templates
window.switchTab = switchTab;
window.showBadgePopup = showBadgePopup;
window.triggerConfetti = triggerConfetti;
