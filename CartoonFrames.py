import cv2
import numpy as np
import tensorflow as tf
from PreprocessFrames import load_image, preprocess_image

def cartoon(image_path):
    # Load and preprocess the input image
    input_image = load_image(image_path)  # Load image and normalize to [-1, 1]
    preprocessed_image = preprocess_image(input_image, target_dim=512)  # Resize to 512x512
    preprocessed_image = tf.convert_to_tensor(preprocessed_image)

    # Load the TensorFlow Lite model
    model_path = "model.tflite"  # Path to the TFLite model
    interpreter = tf.lite.Interpreter(model_path=model_path)

    # Allocate tensors and get input/output details
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # Set the input tensor for the model
    interpreter.set_tensor(input_details[0]['index'], preprocessed_image)

    # Run inference
    interpreter.invoke()

    # Get the model output
    output_tensor = interpreter.get_tensor(output_details[0]['index'])

    # Post-process the model output to generate the cartoonized image
    cartoon_image = (np.squeeze(output_tensor) + 1.0) * 127.5  # Denormalize from [-1, 1] to [0, 255]
    cartoon_image = np.clip(cartoon_image, 0, 255).astype(np.uint8)  # Ensure valid pixel range

    return cartoon_image

