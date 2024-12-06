import cv2
import numpy as np
import tensorflow as tf

# Load image from path or process input data directly
def load_image(image_path):
    # Check if the input is a string (path) or an array (preloaded data)
    print(type(image_path))
    if isinstance(image_path, str):
        # Read the image from the specified path
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Image not found or could not be read at {image_path}")
    elif isinstance(image_path, np.ndarray):
        # Directly use the image array if passed
        image = image_path
    else:
        # Raise an error if the input type is neither a string nor an array
        raise TypeError("Input must be a string (path) or a NumPy array (image).")
    
    # Convert the image to float32 and normalize to [-1, 1]
    image_normalized = image.astype(np.float32) / 127.5 - 1
    
    # Add a batch dimension
    image_batched = np.expand_dims(image_normalized, axis=0)
    
    # Convert to TensorFlow tensor
    image_tensor = tf.convert_to_tensor(image_batched)
    
    return image_tensor

# Preprocess image by resizing and cropping
def preprocess_image(image_tensor, target_dim=224):
    # Get the height and width of the image
    original_shape = tf.cast(tf.shape(image_tensor)[1:-1], tf.float32)
    
    # Calculate the smallest dimension and scale factor
    smallest_dimension = tf.reduce_min(original_shape)
    scale_factor = target_dim / smallest_dimension
    
    # Compute the new shape after scaling
    new_shape = tf.cast(original_shape * scale_factor, tf.int32)
    
    # Resize the image while maintaining aspect ratio
    resized_image = tf.image.resize(image_tensor, new_shape)
    
    # Crop or pad the image to the target dimensions
    final_image = tf.image.resize_with_crop_or_pad(resized_image, target_dim, target_dim)
    
    return final_image
