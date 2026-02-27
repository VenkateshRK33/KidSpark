// Canvas Drawing Functionality for Stage 4

let canvas, ctx;
let isDrawing = false;
let currentColor = '#000000';
let currentSize = 5;
let isEraser = false;
let startTime = Date.now();

function initCanvas() {
    canvas = document.getElementById('drawingCanvas');
    if (!canvas) return;
    
    ctx = canvas.getContext('2d');
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    
    // Set white background
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw light grid
    drawGrid();
    
    // Mouse events
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mousemove', draw);
    canvas.addEventListener('mouseup', stopDrawing);
    canvas.addEventListener('mouseout', stopDrawing);
    
    // Touch events for mobile
    canvas.addEventListener('touchstart', handleTouch);
    canvas.addEventListener('touchmove', handleTouch);
    canvas.addEventListener('touchend', stopDrawing);
    
    // Color picker
    document.querySelectorAll('.color-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            currentColor = this.dataset.color;
            isEraser = false;
            document.getElementById('eraserBtn').classList.remove('active');
        });
    });
    
    // Set first color as active
    document.querySelector('.color-btn').classList.add('active');
    
    // Brush sizes
    document.getElementById('smallBrush').addEventListener('click', function() {
        setBrushSize(2, this);
    });
    document.getElementById('mediumBrush').addEventListener('click', function() {
        setBrushSize(5, this);
    });
    document.getElementById('largeBrush').addEventListener('click', function() {
        setBrushSize(10, this);
    });
    
    // Eraser
    document.getElementById('eraserBtn').addEventListener('click', function() {
        isEraser = !isEraser;
        this.classList.toggle('active');
        if (isEraser) {
            document.querySelectorAll('.color-btn').forEach(b => b.classList.remove('active'));
        }
    });
    
    // Clear button
    document.getElementById('clearBtn').addEventListener('click', clearCanvas);
    
    // Start timer
    startTimer();
    
    // On form submit, save canvas data
    document.getElementById('stage4Form').addEventListener('submit', function(e) {
        const drawingData = canvas.toDataURL('image/png');
        document.getElementById('drawingData').value = drawingData;
        
        const timeSpent = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById('drawingTime').value = timeSpent;
    });
}

function drawGrid() {
    ctx.strokeStyle = '#f0f0f0';
    ctx.lineWidth = 1;
    
    for (let i = 0; i < canvas.width; i += 20) {
        ctx.beginPath();
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvas.height);
        ctx.stroke();
    }
    
    for (let i = 0; i < canvas.height; i += 20) {
        ctx.beginPath();
        ctx.moveTo(0, i);
        ctx.lineTo(canvas.width, i);
        ctx.stroke();
    }
}

function setBrushSize(size, btn) {
    currentSize = size;
    document.querySelectorAll('.tool-btn').forEach(b => {
        if (b.id.includes('Brush')) b.classList.remove('active');
    });
    btn.classList.add('active');
}

function startDrawing(e) {
    isDrawing = true;
    const pos = getMousePos(e);
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
}

function draw(e) {
    if (!isDrawing) return;
    
    const pos = getMousePos(e);
    
    ctx.strokeStyle = isEraser ? 'white' : currentColor;
    ctx.lineWidth = isEraser ? 20 : currentSize;
    
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
}

function stopDrawing() {
    isDrawing = false;
}

function getMousePos(e) {
    const rect = canvas.getBoundingClientRect();
    return {
        x: e.clientX - rect.left,
        y: e.clientY - rect.top
    };
}

function handleTouch(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const mouseEvent = new MouseEvent(e.type === 'touchstart' ? 'mousedown' : 'mousemove', {
        clientX: touch.clientX,
        clientY: touch.clientY
    });
    canvas.dispatchEvent(mouseEvent);
}

function clearCanvas() {
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    drawGrid();
}

function startTimer() {
    const timerDisplay = document.getElementById('canvasTimer');
    if (!timerDisplay) return;
    
    setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        timerDisplay.textContent = elapsed;
    }, 1000);
}

// Initialize canvas when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCanvas);
} else {
    initCanvas();
}
