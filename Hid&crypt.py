import cv2
import sys
from Crypto.Cipher import AES

def pad(data):
    # Pads the data to a multiple of 16 bytes using PKCS#7 padding
    pad_length = 16 - len(data) % 16
    return data + bytes([pad_length] * pad_length)

def unpad(data):
    # Removes the PKCS#7 padding from the data
    return data[:-data[-1]]

def encode_text_in_image(image, text, password):
    # Encrypt the text using AES
    cipher = AES.new(password, AES.MODE_ECB)
    encrypted_text = cipher.encrypt(pad(text.encode()))
    
    # Convert the image to a 3-channel BGR image
    image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    # Convert the encrypted text to a list of integers
    encrypted_text_int = [int(b) for b in encrypted_text]
    
    # Encode the encrypted text in the least significant bits of the image pixels
    for i, value in enumerate(encrypted_text_int):
        # Get the i-th pixel value
        pixel = image[i // image.shape[1], i % image.shape[1]]
        
        # Set the least significant bit of each channel to the corresponding
        # bit of the value
        pixel[0] = (pixel[0] & 0xFE) | (value & 0x01)
        pixel[1] = (pixel[1] & 0xFE) | ((value & 0x02) >> 1)
        pixel[2] = (pixel[2] & 0xFE) | ((value & 0x04) >> 2)
        
        # Update the i-th pixel value
        image[i // image.shape[1], i % image.shape[1]] = pixel
        
    return image

def decode_text_from_image(image, password):
    # Convert the image to a 1-channel grayscale image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Initialize an empty list to store the decoded values
    decrypted_text_int = []
    
    # Decode the encrypted text from the least significant bits of the image pixels
    for i in range(image.shape[0] * image.shape[1]):
        # Get the i-th pixel value
        pixel = image[i // image.shape[1], i % image.shape[1]]
        
        # Extract the least significant bits of each channel
          # If the value is 0, we have reached the end of the encrypted text
        if value == 0:
            break
            
        # Add the value to the list
        decrypted_text_int.append(value)
    
    # Decrypt the encrypted text using AES
    cipher = AES.new(password, AES.MODE_ECB)
    decrypted_text = unpad(cipher.decrypt(bytes(decrypted_text_int)))
    
    # Convert the decrypted text to a string
    text = decrypted_text.decode()
    
    return text

# Read the image
image = cv2.imread('image.jpg', cv2.IMREAD_GRAYSCALE)

# Check if the -d flag is present to decode the text
if '-d' in sys.argv:
    password = input('Enter the password: ')
    text = decode_text_from_image(image, password)
    print(text)

# Check if the -e flag is present to encode the text
if '-e' in sys.argv:
    password = input('Enter the password: ')
    text = input('Enter the text to be hidden: ')
    image_with_hidden_text = encode_text_in_image(image, text, password)
    cv2.imwrite('image_with_hidden_text.jpg', image_with_hidden_text)
      value = (pixel[0] & 0x01) | ((pixel[1] & 0x01) << 1) | ((pixel[2] & 0x01) <<
