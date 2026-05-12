from tensorflow.keras import layers, models

def build_model():
    """
    Defines a Convolutional Neural Network (CNN) architecture 
    for binary image classification (Real vs Fake).
    """
    model = models.Sequential([
        # Initial Convolutional Block
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        layers.MaxPooling2D((2, 2)),

        # Second Convolutional Block
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        # Third Convolutional Block
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),

        # Flattening and Dense Layers
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.5),  # Regularization to prevent overfitting
        layers.Dense(1, activation='sigmoid') # Binary Output: 0 (Fake) or 1 (Real)
    ])
    
    return model