import numpy as np, os
from PIL import Image, ImageDraw

def generate_art_drawing(size=64):
    img = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(img)
    
    # Random curves
    for _ in range(np.random.randint(3, 8)):
        x1, y1 = np.random.randint(0, size-10), np.random.randint(0, size-10)
        x2, y2 = x1 + np.random.randint(10, 30), y1 + np.random.randint(10, 30)
        x2, y2 = min(x2, size-1), min(y2, size-1)
        draw.arc([x1, y1, x2, y2], 0, np.random.randint(180, 360), fill=0, width=2)
    
    # Random blobs
    for _ in range(np.random.randint(2, 5)):
        cx, cy, r = np.random.randint(5, 59), np.random.randint(5, 59), np.random.randint(3, 15)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=np.random.randint(0, 150))
    
    return np.array(img, dtype=np.float32) / 255.0

def generate_sports_sketch(size=64):
    img = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(img)
    
    # Circle (ball)
    cx, cy, r = size//2, size//2, np.random.randint(12, 22)
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=0, width=2)
    
    # Straight lines
    for _ in range(np.random.randint(2, 5)):
        x1, x2 = np.random.randint(0, size), np.random.randint(0, size)
        draw.line([x1, 0, x2, size], fill=0, width=2)
    
    return np.array(img, dtype=np.float32) / 255.0

def generate_academic_diagram(size=64):
    img = Image.new('L', (size, size), 255)
    draw = ImageDraw.Draw(img)
    
    # Grid pattern
    step = size // 4
    for i in range(0, size, step):
        draw.line([i, 0, i, size], fill=180, width=1)
        draw.line([0, i, size, i], fill=180, width=1)
    
    # Geometric shapes
    pts = [(np.random.randint(5, 59), np.random.randint(5, 59)) for _ in range(np.random.randint(3, 6))]
    if len(pts) >= 2:
        draw.line(pts, fill=0, width=2)
    
    return np.array(img, dtype=np.float32) / 255.0

def generate_dataset(n_per_class=600, save_dir='data/cnn_data'):
    os.makedirs(f'{save_dir}/art', exist_ok=True)
    os.makedirs(f'{save_dir}/sports', exist_ok=True)
    os.makedirs(f'{save_dir}/academic', exist_ok=True)
    
    generators = [
        ('art', generate_art_drawing),
        ('sports', generate_sports_sketch),
        ('academic', generate_academic_diagram)
    ]
    
    for label, gen_fn in generators:
        for i in range(n_per_class):
            arr = gen_fn()
            img = Image.fromarray((arr * 255).astype(np.uint8))
            img.save(f'{save_dir}/{label}/{label}_{i:04d}.png')
    
    print(f'Generated {n_per_class * 3} images in {save_dir}/')

if __name__ == '__main__':
    generate_dataset()
