// Detection Game JavaScript

// ============================================
// STAGE 1: Character Selection
// ============================================
function initStage1() {
    const cards = document.querySelectorAll('.character-card');
    const submitBtn = document.getElementById('submitBtn');
    const avatarInput = document.getElementById('avatarInput');
    const progressBar = document.querySelector('.progress-fill');
    
    // Animate progress bar
    setTimeout(() => {
        const progress = document.querySelector('.progress-bar').dataset.progress;
        progressBar.style.width = progress + '%';
    }, 100);
    
    // Fade in cards with delay
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Card selection
    cards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove selected from all cards
            cards.forEach(c => c.classList.remove('selected'));
            
            // Add selected to clicked card
            this.classList.add('selected');
            
            // Store avatar value
            const avatar = this.dataset.avatar;
            avatarInput.value = avatar;
            
            // Enable submit button
            submitBtn.disabled = false;
        });
    });
}

// ============================================
// STAGE 2: Scenario Navigation
// ============================================
function initStage2(totalScenarios) {
    let currentScenario = 1;
    const slides = document.querySelectorAll('.scenario-slide');
    const nextBtns = document.querySelectorAll('.next-btn');
    const scenarioCounter = document.getElementById('currentScenario');
    const form = document.getElementById('stage2Form');
    const progressBar = document.querySelector('.progress-fill');
    
    // Animate progress bar
    setTimeout(() => {
        const progress = document.querySelector('.progress-bar').dataset.progress;
        progressBar.style.width = progress + '%';
    }, 100);
    
    // Choice selection
    document.querySelectorAll('.choice-card').forEach(card => {
        card.addEventListener('click', function() {
            const slide = this.closest('.scenario-slide');
            const choices = slide.querySelectorAll('.choice-card');
            
            // Remove selected from all choices in this scenario
            choices.forEach(c => c.classList.remove('selected'));
            
            // Add selected to clicked choice
            this.classList.add('selected');
            
            // Store value in hidden input
            const field = this.dataset.field;
            const value = this.dataset.value;
            const input = document.getElementById(field + 'Input');
            if (input) {
                input.value = value;
            }
            
            // Enable next button or submit button
            const nextBtn = slide.querySelector('.next-btn');
            const submitBtn = slide.querySelector('.submit-btn');
            if (nextBtn) {
                nextBtn.disabled = false;
            }
            if (submitBtn) {
                submitBtn.disabled = false;
            }
        });
    });
    
    // Next button navigation
    nextBtns.forEach((btn, index) => {
        btn.addEventListener('click', function() {
            if (currentScenario < totalScenarios) {
                // Hide current slide
                slides[currentScenario - 1].classList.remove('active');
                slides[currentScenario - 1].classList.add('slide-out');
                
                // Show next slide
                currentScenario++;
                slides[currentScenario - 1].classList.add('active');
                slides[currentScenario - 1].classList.add('slide-in');
                
                // Update counter
                scenarioCounter.textContent = currentScenario;
                
                // Remove animation classes after animation
                setTimeout(() => {
                    slides.forEach(s => {
                        s.classList.remove('slide-in', 'slide-out');
                    });
                }, 500);
            }
        });
    });
}

// ============================================
// STAGE 3: Tapping Game with Timer
// ============================================
function initStage3(timerDuration) {
    const cards = document.querySelectorAll('.hobby-card');
    const timerDisplay = document.getElementById('timerDisplay');
    const selectedCount = document.getElementById('selectedCount');
    const form = document.getElementById('stage3Form');
    const progressBar = document.querySelector('.progress-fill');
    
    let timeLeft = timerDuration;
    let selectedItems = [];
    let timerInterval;
    
    // Animate progress bar
    setTimeout(() => {
        const progress = document.querySelector('.progress-bar').dataset.progress;
        progressBar.style.width = progress + '%';
    }, 100);
    
    // Start timer
    timerInterval = setInterval(() => {
        timeLeft--;
        timerDisplay.textContent = timeLeft;
        
        // Change color when below 10 seconds
        if (timeLeft <= 10) {
            timerDisplay.classList.add('timer-warning');
        }
        
        // Auto-submit when timer reaches 0
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            submitForm();
        }
    }, 1000);
    
    // Card tap/click
    cards.forEach(card => {
        card.addEventListener('click', function() {
            const hobby = this.dataset.hobby;
            
            if (this.classList.contains('selected')) {
                // Deselect
                this.classList.remove('selected');
                selectedItems = selectedItems.filter(item => item !== hobby);
            } else {
                // Select
                this.classList.add('selected');
                selectedItems.push(hobby);
                
                // Confetti effect
                createConfetti(this);
            }
            
            // Update counter
            selectedCount.textContent = selectedItems.length;
        });
    });
    
    // Form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        clearInterval(timerInterval);
        submitForm();
    });
    
    function submitForm() {
        // Create hidden inputs for all selected items
        selectedItems.forEach(item => {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'tapped_items';
            input.value = item;
            form.appendChild(input);
        });
        
        form.submit();
    }
    
    function createConfetti(element) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti-pop';
        confetti.textContent = '✨';
        element.appendChild(confetti);
        
        setTimeout(() => {
            confetti.remove();
        }, 600);
    }
}

// ============================================
// General Progress Bar Animation
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.querySelector('.progress-fill');
    if (progressBar) {
        setTimeout(() => {
            const progress = document.querySelector('.progress-bar').dataset.progress;
            progressBar.style.width = progress + '%';
        }, 100);
    }
});


// ============================================
// STAGE 4: Drawing/Sports/Puzzle Simulation
// ============================================
function initStage4(simType) {
    const progressBar = document.querySelector('.progress-fill');
    
    // Animate progress bar
    setTimeout(() => {
        const progress = document.querySelector('.progress-bar').dataset.progress;
        progressBar.style.width = progress + '%';
    }, 100);
    
    if (simType === 'sports') {
        initSportsSimulation();
    } else if (simType === 'puzzle') {
        initPuzzleSimulation();
    }
    // Drawing is handled by canvas.js
}

function initSportsSimulation() {
    let fieldersPlaced = 0;
    const maxFielders = 3;
    const placedPositions = [];
    
    document.querySelectorAll('.fielder-btn').forEach(btn => {
        btn.style.cssText += 'width: 60px; height: 60px; border-radius: 50%; background: white; border: 3px solid #333; font-size: 1.5rem; font-weight: 700; cursor: pointer;';
        
        btn.addEventListener('click', function() {
            const position = this.dataset.position;
            
            if (placedPositions.includes(position)) {
                // Remove fielder
                this.style.background = 'white';
                this.style.color = '#333';
                placedPositions.splice(placedPositions.indexOf(position), 1);
                fieldersPlaced--;
            } else if (fieldersPlaced < maxFielders) {
                // Place fielder
                this.style.background = '#4caf50';
                this.style.color = 'white';
                placedPositions.push(position);
                fieldersPlaced++;
            }
            
            document.getElementById('fieldersCount').textContent = fieldersPlaced;
            document.getElementById('puzzleScore').value = fieldersPlaced + 1;
            
            // Enable submit when 3 fielders placed
            document.getElementById('stage4Submit').disabled = fieldersPlaced < 3;
        });
    });
}

function initPuzzleSimulation() {
    const puzzles = [
        { question: '2 + 3 = ?', answer: 5 },
        { question: '10 - 4 = ?', answer: 6 },
        { question: '3 × 3 = ?', answer: 9 },
        { question: '8 ÷ 2 = ?', answer: 4 },
        { question: '15 - 7 = ?', answer: 8 }
    ];
    
    let currentPuzzle = 0;
    let correctAnswers = 0;
    
    const puzzleText = document.getElementById('puzzleText');
    const puzzleNum = document.getElementById('puzzleNum');
    
    // Style number buttons
    document.querySelectorAll('.num-btn').forEach(btn => {
        btn.style.cssText = 'padding: 20px; font-size: 1.5rem; font-weight: 700; background: #667eea; color: white; border: none; border-radius: 10px; cursor: pointer;';
        
        btn.addEventListener('click', function() {
            const answer = parseInt(this.dataset.num);
            
            if (answer === puzzles[currentPuzzle].answer) {
                correctAnswers++;
                this.style.background = '#4caf50';
            } else {
                this.style.background = '#f44336';
            }
            
            setTimeout(() => {
                currentPuzzle++;
                
                if (currentPuzzle < puzzles.length) {
                    puzzleText.textContent = puzzles[currentPuzzle].question;
                    puzzleNum.textContent = currentPuzzle + 1;
                    document.querySelectorAll('.num-btn').forEach(b => b.style.background = '#667eea');
                } else {
                    // All puzzles done
                    document.getElementById('puzzleScore').value = correctAnswers;
                    document.getElementById('stage4Submit').disabled = false;
                    puzzleText.textContent = `Great job! You got ${correctAnswers}/5 correct!`;
                    document.querySelector('.number-pad').style.display = 'none';
                }
            }, 500);
        });
    });
}

// ============================================
// STAGE 5: Final Questions
// ============================================
function initStage5(totalQuestions) {
    let currentQuestion = 1;
    const slides = document.querySelectorAll('.question-slide');
    const dots = document.querySelectorAll('.dot');
    const progressBar = document.querySelector('.progress-fill');
    
    // Animate progress bar
    setTimeout(() => {
        const progress = document.querySelector('.progress-bar').dataset.progress;
        progressBar.style.width = progress + '%';
    }, 100);
    
    // Update active dot
    function updateDots() {
        dots.forEach((dot, index) => {
            if (index < currentQuestion) {
                dot.style.background = 'white';
            } else {
                dot.style.background = 'rgba(255,255,255,0.3)';
            }
        });
    }
    
    updateDots();
    
    // Choice selection
    document.querySelectorAll('.choice-card').forEach(card => {
        card.addEventListener('click', function() {
            const slide = this.closest('.question-slide');
            const choices = slide.querySelectorAll('.choice-card');
            
            // Remove selected from all choices in this question
            choices.forEach(c => c.classList.remove('selected'));
            
            // Add selected to clicked choice
            this.classList.add('selected');
            
            // Store value in hidden input
            const field = this.dataset.field;
            const value = this.dataset.value;
            const input = document.getElementById(field + 'Input');
            if (input) {
                input.value = value;
            }
            
            // Enable next/submit button
            const nextBtn = slide.querySelector('.next-btn');
            const submitBtn = slide.querySelector('.submit-btn');
            if (nextBtn) {
                nextBtn.disabled = false;
            }
            if (submitBtn) {
                submitBtn.disabled = false;
            }
        });
    });
    
    // Next button navigation
    document.querySelectorAll('.next-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            if (currentQuestion < totalQuestions) {
                // Hide current slide
                slides[currentQuestion - 1].classList.remove('active');
                slides[currentQuestion - 1].classList.add('slide-out');
                
                // Show next slide
                currentQuestion++;
                slides[currentQuestion - 1].classList.add('active');
                slides[currentQuestion - 1].classList.add('slide-in');
                
                // Update dots
                updateDots();
                
                // Remove animation classes after animation
                setTimeout(() => {
                    slides.forEach(s => {
                        s.classList.remove('slide-in', 'slide-out');
                    });
                }, 500);
            }
        });
    });
}
