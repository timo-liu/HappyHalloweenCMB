"""
Design specifications

1. Detect face
2. If face detected, play happy_halloween()

happy_halloween()
draw an image
play a sound
create a chat window
"""

import cv2
import pygame
import pyttsx3

is_playing = False
face_detected = False
TIMEOUT = 1000
engine = None

pygame.init()

# happy halloween
COMBEBACK_TEXT = "Come back please I haven't finished my spiel"
WELCOME_TEXT = "THE CORINA NEUROLINGUISTICS LAB WISHES YOU A HAPPY HALLOWEEN!"
DISPLAYED_WELCOME = ""
text_idx = 0
typing_speed = 50
last_update = pygame.time.get_ticks()
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
screen_size = pygame.display.Info()
screen_width = screen_size.current_w
screen_height = screen_size.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Happy Halloween!")

def render_wrapped_text(text, font, color, max_width):
    """Return a surface with automatically wrapped text."""
    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)

    # Render each line
    surfaces = [font.render(line.strip(), True, color) for line in lines]
    return surfaces

def face_cap():
    global is_playing
    global TIMEOUT
    global face_detected
    global engine
    global COMBEBACK_TEXT
    global WELCOME_TEXT
    global DISPLAYED_WELCOME
    global text_idx
    global typing_speed
    global last_update
    global font
    global clock
    global screen_size
    global screen_width
    global screen_height
    global screen
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) <= 0:
            face_detected = False

        if len(faces) > 0 and not is_playing:
            face_detected = True
            is_playing = True
        if face_detected:
            happy_halloween()
        else:
            if (text_idx < len(WELCOME_TEXT)):
                engine.say(COMBEBACK_TEXT)
                engine.runAndWait()

def happy_halloween():
    global is_playing
    global TIMEOUT
    global engine
    global COMBEBACK_TEXT
    global WELCOME_TEXT
    global DISPLAYED_WELCOME
    global text_idx
    global typing_speed
    global last_update
    global font
    global clock
    global screen_size
    global screen_width
    global screen_height
    global screen
    pygame.display.set_caption("Happy Halloween!")
    # typing
    now = pygame.time.get_ticks()
    if text_idx < len(WELCOME_TEXT) and now - last_update > typing_speed:
        DISPLAYED_WELCOME += WELCOME_TEXT[text_idx]
        text_idx += 1
        last_update = now

    screen.fill((30, 30, 30))
    text_surfaces = render_wrapped_text(DISPLAYED_WELCOME, font, (255, 255, 255), screen_width - 100)
    y = 100
    for text_surface in text_surfaces:
        screen.blit(text_surface, (100, y))
        y += text_surface.get_height() + 5

    pygame.display.flip()
    clock.tick(60)



if __name__ == '__main__':
    engine = pyttsx3.init()
    face_cap()