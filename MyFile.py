import numpy as np
import cv2
from google.colab import files

# Function to embed watermark
def embed_watermark(image_path, watermark_text, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Error: Unable to load image at {image_path}")
    
    # Convert the watermark text into binary
    binary_watermark = ''.join(format(ord(char), '08b') for char in watermark_text)

    # Check if watermark fits in the image
    total_bits_needed = len(binary_watermark)
    total_pixels = image.size // 8  # Each pixel has 3 channels, 24 bits
    if total_bits_needed > total_pixels:
        raise ValueError("Watermark too large for the image.")

    # Embed watermark in the least significant bits (LSB) of the image
    watermark_index = 0
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for c in range(3):  # Iterate over 3 channels (BGR)
                if watermark_index < total_bits_needed:
                    # Modify the LSB of each channel
                    image[i, j, c] = (image[i, j, c] & 0xFE) | int(binary_watermark[watermark_index])
                    watermark_index += 1

    # Save the image with embedded watermark
    cv2.imwrite(output_path, image)
    print(f"Watermark embedded successfully! Image saved to {output_path}")

# Function to extract watermark
def extract_watermark(image_path, watermark_length):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Error: Unable to load image at {image_path}")

    # Extract the least significant bits (LSB) from the image
    binary_watermark = ''
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            for c in range(3):  # Iterate over 3 channels (BGR)
                binary_watermark += str(image[i, j, c] & 1)

    # Convert the binary string back to text
    extracted_text = ''
    for i in range(0, watermark_length * 8, 8):
        byte = binary_watermark[i:i+8]
        extracted_text += chr(int(byte, 2))

    return extracted_text

# Test the watermarking system
if __name__ == "__main__":
    # Upload the image from local machine
    uploaded = files.upload()

    # Get the image file name from the uploaded files
    input_image_path = list(uploaded.keys())[0]  # Get the first uploaded file name

    watermark_text = input("Enter the watermark text: ")  # User input for watermark text
    output_image_path = input("Enter the path to save the watermarked image (e.g., 'output_image.png'): ")

    try:
        # Embed watermark into the image
        embed_watermark(input_image_path, watermark_text, output_image_path)

        # Extract watermark from the watermarked image
        extracted_watermark = extract_watermark(output_image_path, len(watermark_text))
        print(f"Extracted watermark: {extracted_watermark}")
    except Exception as e:
        print(f"An error occurred: {e}")

