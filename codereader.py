import cv2
from pyzbar.pyzbar import decode

# ucitavanje fajla
img = cv2.imread('kod.png')

# spremanje skeniranog koda u txt fajl
with open('scanned_codes.txt', 'w') as file:
    # Dekodiranje koda sa slike
    for code in decode(img):
        code_type = code.type
        code_data = code.data.decode('utf-8')

        # Ispis koda
        print("Type:", code_type)
        print("Data:", code_data)

        file.write(f"Type: {code_type}\n")
        file.write(f"Data: {code_data}\n\n")
