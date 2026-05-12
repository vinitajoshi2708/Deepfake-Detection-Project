import tensorflow as tf
import os
from model import build_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# 1. Configuration and Hyperparameters
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 25  # Extended training for higher accuracy
DATASET_PATH = 'dataset'

# 2. Data Preparation and Augmentation
print("[INFO] Initializing data generators...")
datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

train_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='training'
)

validation_generator = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary',
    subset='validation'
)

# 3. Model Compilation
print("[INFO] Compiling CNN architecture...")
model = build_model()
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# 4. Training Execution
print(f"[INFO] Starting training for {EPOCHS} epochs. Please monitor loss and accuracy metrics...")
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

# 5. Model Export
if not os.path.exists('saved_model'):
    os.makedirs('saved_model')

print("[INFO] Saving the trained weights...")
model.save('saved_model/model.h5')
print("[SUCCESS] Training cycle complete. Model saved to 'saved_model/model.h5'.")