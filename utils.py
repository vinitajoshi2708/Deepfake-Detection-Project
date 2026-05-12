import numpy as np
from tensorflow.keras.preprocessing import image

def preprocess_image(img_path):
    """Resizes and normalizes image for the model."""
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Rescale to [0,1]
    return img_array