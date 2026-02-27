import numpy as np, os, pickle
from PIL import Image

def load_images(data_dir='data/cnn_data'):
    X, y = [], []
    for label_idx, label in enumerate(['art', 'sports', 'academic']):
        folder = os.path.join(data_dir, label)
        for fname in os.listdir(folder):
            if fname.endswith('.png'):
                img = Image.open(os.path.join(folder, fname)).convert('L').resize((64, 64))
                X.append(np.array(img, dtype=np.float32) / 255.0)
                y.append(label_idx)
    return np.array(X).reshape(-1, 64, 64, 1), np.array(y)

def build_and_train():
    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
    from tensorflow.keras.utils import to_categorical
    from sklearn.model_selection import train_test_split
    
    X, y = load_images()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    y_train_cat = to_categorical(y_train, 3)
    y_test_cat = to_categorical(y_test, 3)
    
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 1)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(3, activation='softmax')
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    model.fit(X_train, y_train_cat, epochs=15, batch_size=32, 
              validation_data=(X_test, y_test_cat), verbose=1)
    
    loss, acc = model.evaluate(X_test, y_test_cat)
    print(f'CNN Test Accuracy: {acc:.4f}')
    
    model.save('ml/models/drawing_cnn.h5')
    print('Saved: ml/models/drawing_cnn.h5')

if __name__ == '__main__':
    build_and_train()
