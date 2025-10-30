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

is_playing = False
TIMEOUT = 1000

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
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0 and not is_playing:
            is_playing = True
            print("playing")
            happy_halloween()

def happy_halloween():
    global is_playing
    global TIMEOUT

    pygame.init()

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
    # typing
    while True:
        now = pygame.time.get_ticks()
        if text_idx < len(WELCOME_TEXT) and now - last_update > typing_speed:
            DISPLAYED_WELCOME += WELCOME_TEXT[text_idx]
            text_idx += 1
            last_update = now

            finished_time = None

        screen.fill((30, 30, 30))
        text_surfaces = render_wrapped_text(DISPLAYED_WELCOME, font, (255, 255, 255), screen_width - 100)
        y = 100
        for text_surface in text_surfaces:
            screen.blit(text_surface, (100, y))
            y += text_surface.get_height() + 5

        if text_idx == len(WELCOME_TEXT) and finished_time is None:
             finished_time = now

        if finished_time and now - finished_time > TIMEOUT:
            pygame.quit()
            is_playing = False
            break
        pygame.display.flip()
        clock.tick(60)



if __name__ == '__main__':
    face_cap()