from PIL import Image
import numpy as np
import os

# Function to encode a message into an image
def encode_message(image_path, message, output_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")

    # Open the image and ensure it's in RGB format
    img = Image.open(image_path).convert("RGB")
    pixels = np.array(img, dtype=np.uint8)  # Ensure uint8 format

    # Append a null character to mark the end of the message
    message += chr(0)
    binary_message = ''.join(format(ord(char), '08b') for char in message)

    # Ensure the message fits in the image
    if len(binary_message) > pixels.size:
        raise ValueError("Message too long to hide in this image!")

    # Flatten the pixel array
    flat_pixels = pixels.flatten().astype(np.uint8)  # Explicitly cast to uint8

    # Modify the least significant bit (LSB) for each pixel
    for i in range(len(binary_message)):
        flat_pixels[i] = (flat_pixels[i] & 0b11111110) | int(binary_message[i])

    # Reshape back to the original image shape and save it
    encoded_pixels = flat_pixels.reshape(pixels.shape)
    encoded_img = Image.fromarray(encoded_pixels)
    encoded_img.save(output_path)

    print(f"✅ Message successfully encoded into '{output_path}'")


if __name__ == "__main__":
    # Get user input
    img_path = input("Enter the path to the input image: ")  # User provides image path
    out_path = input("Enter the path for the output image: ")  # User provides output path
    secret_msg = input("Enter the secret message: ")  # User enters the secret message

    # Encode the message
    encode_message(img_path, secret_msg, out_path)
    print(f"✅ Message encoded and saved as {out_path}")

