#!/usr/bin/python3

import cv2
import sys

def encode_text_in_image(image, text):
    # Convert the image to a 3-channel BGR image
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    # Convert the text to a list of ASCII values
    text_ascii = [ord(c) for c in text]
    
    # Encode the text in the least significant bits of the image pixels
    for i, ascii_value in enumerate(text_ascii):
        # Get the i-th pixel value
        pixel = image[i // image.shape[1], i % image.shape[1]]
        
        # Set the least significant bit of each channel to the corresponding
        # bit of the ASCII value
        pixel[0] = (pixel[0] & 0xFE) | (ascii_value & 0x01)
        pixel[1] = (pixel[1] & 0xFE) | ((ascii_value & 0x02) >> 1)
        pixel[2] = (pixel[2] & 0xFE) | ((ascii_value & 0x04) >> 2)
        
        # Update the i-th pixel value
        image[i // image.shape[1], i % image.shape[1]] = pixel
        
    return image

def decode_text_from_image(image):
    # Convert the image to a 1-channel grayscale image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Initialize an empty list to store the decoded ASCII values
    text_ascii = []
    
    # Decode the text from the least significant bits of the image pixels
    for i in range(image.shape[0] * image.shape[1]):
        # Get the i-th pixel value
        pixel = image[i // image.shape[1], i % image.shape[1]]
        
        # Extract the least significant bits of each channel
        ascii_value = (pixel[0] & 0x01) | ((pixel[1] & 0x01) << 1) | ((pixel[2] & 0x01) << 2)
        
        # If the ASCII value is 0, we have reached the end of the text
        if ascii_value == 0:
            break
            
        # Add the ASCII value to the list
        text_ascii.append(ascii_value)
    
    # Convert the list of ASCII values to a string
    text = ''.join(chr(c) for c in text_ascii)
    
    return text

# Read the image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)


# Check if the -d flag is present to decode the text
if '-d' in sys.argv:
    text = decode_text_from_image(image)
    print(text)

# Check if the -e flag is present to encode the text
if '-e' in sys.argv:
    text = input('Enter the text to be hidden: ')
    image_with_hidden_text = encode_text_in_image(image, text)
    cv2.imwrite('image_with_hidden_text.jpg', image_with_hidden_text)
