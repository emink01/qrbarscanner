import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import os
import pygame

# Funkcija za 'beep' zvuk
def play_beep(mp3_file):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Error: {e}")

# Inicijalizacija web kamere
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # sirina
cap.set(4, 480)  # visina

# kreiranje foldera sa spremljenim slikama kodova
folder_name = 'scanned_images'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Set se koristi za praćenje kodova koji su duplikati
scanned_codes = set()

# Otvaranje txt fajla za spremanje dekodiranih podataka
with open('scanned_codes.txt', 'a') as file:  
    camera = True
    while camera:
        success, frame = cap.read()  # spremi frame iz kamere

        if success:
            ## Privremeni skup za praćenje kodova otkrivenih u trenutnom frame-u
            detected_codes = set()

            for code in decode(frame):
                code_type = code.type
                code_data = code.data.decode('utf-8')
                
                # Provjeri da li je kod već procesuiran u ovom frame-u
                if code_data not in detected_codes:
                    detected_codes.add(code_data)
                    
                    # Provjeri da li je kod već procesuiran ranije
                    if code_data not in scanned_codes:
                        scanned_codes.add(code_data)

                        # Uzmi timestamp
                        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

                        # Spremi sliku sa qr kodom
                        image_name = os.path.join(folder_name, f'scanned_image_{timestamp}.png')
                        cv2.imwrite(image_name, frame)

                        # upis podataka
                        file.write(f"Type: {code_type}\n")
                        file.write(f"Data: {code_data}\n")
                        file.write(f"Timestamp: {timestamp}\n")
                        file.write(f"Image: {image_name}\n\n")

                        # funkcija za zvuk
                        play_beep('beep.mp3')

                        # feedback
                        cv2.putText(frame, 'QR Code Scanned!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow('Testing-code-scan', frame)

        # izadji pritiskom na tipku q
        if cv2.waitKey(1) & 0xFF == ord('q'):
            camera = False

# zatvaranje prozora
cap.release()
cv2.destroyAllWindows()
