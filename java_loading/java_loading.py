import pygame
import sys
from pygame import gfxdraw
from PIL import Image
import numpy as np
import os
import requests

pygame.init()

laad_scherm = pygame.display.set_mode((300, 100))
pygame.display.set_caption("Installing java ... ")
font = pygame.font.Font(None, 36)
laad_tekst = font.render("Laden ...", True, (0, 0, 0))
tekst_rect = laad_tekst.get_rect(center=(150, 50))
    
laad_scherm.fill((236, 233, 216))
laad_scherm.blit(laad_tekst, tekst_rect)
pygame.display.flip()

WINDOW_WIDTH = 490
WINDOW_HEIGHT = 300
pygame.display.set_caption("Installing java ... ")

video_height = WINDOW_HEIGHT - 60
video_width = int(WINDOW_WIDTH * 0.8)
x_offset = (WINDOW_WIDTH - video_width) // 2

frames_folder = "temp_frames"

def download_coffee_gif():
    url = "https://www.dropbox.com/scl/fi/hjk8t6g44jf8su8ritpok/coffee.gif?rlkey=ak8bf0fhz9i15b8wb7ooqb62d&st=hwzaer5y&dl=1"
    if getattr(sys, 'frozen', False):
        application_path = sys._MEIPASS
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    filename = os.path.join(application_path, "coffee.gif")
    
    if not os.path.exists(filename):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"De {filename} is succesvol gedownload.")
        except requests.exceptions.RequestException as e:
            print(f"Er is een fout opgetreden bij het downloaden: {e}")
    else:
        print(f"De {filename} bestaat al.")
    return filename

def verwerk_video_frames():
    frames = []
    gif = Image.open(download_coffee_gif())
    
    try:
        while True:
            current = gif.resize((video_width, video_height))
            if current.mode != 'RGBA':
                current = current.convert('RGBA')
            frame_string = current.tobytes()
            frame_surface = pygame.image.fromstring(frame_string, current.size, 'RGBA')
            frames.append(frame_surface)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    
    pygame.display.quit()
    return frames

print("Video wordt verwerkt, even geduld...")
download_coffee_gif()
frames = verwerk_video_frames()
total_frames = len(frames)
current_frame = 0

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Installing java ... ")

frame_delay = 1000 // 30
last_frame_time = pygame.time.get_ticks()

clock = pygame.time.Clock()

BACKGROUND = (255, 255, 255)
BORDER = (0, 60, 116)
BAR_COLOR = (0, 180, 0)
BAR_HIGHLIGHT1 = (40, 220, 40)
BAR_HIGHLIGHT2 = (20, 200, 20)
BAR_HIGHLIGHT3 = (10, 190, 10)
BAR_BACKGROUND = (255, 255, 255)

bar_width = WINDOW_WIDTH
bar_height = 20
bar_x = 0
bar_y = WINDOW_HEIGHT - 30
block_width = 12
block_spacing = 5
animation_speed = 2
highlight_height1 = 4
highlight_height2 = 7
highlight_height3 = 10

base_position = bar_x - block_width
num_blocks = 5
total_block_width = block_width + block_spacing
total_width = (num_blocks - 1) * total_block_width + block_width

running = True
while running:
    clock.tick(60)
    current_time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        pass

    if current_time - last_frame_time > frame_delay:
        current_frame = (current_frame + 1) % total_frames
        last_frame_time = current_time

    screen.fill(BACKGROUND)
    screen.blit(frames[current_frame], (x_offset, 10))
    
    pygame.draw.rect(screen, BAR_BACKGROUND, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(screen, BORDER, (bar_x, bar_y, bar_width, bar_height), 1)

    base_position += animation_speed
    if base_position >= bar_x + bar_width + total_width:
        base_position = bar_x - block_width

    for i in range(num_blocks):
        block_x = base_position - (i * total_block_width)
        
        if block_x < bar_x:
            if block_x + block_width > bar_x:
                visible_width = block_x + block_width - bar_x
                pygame.draw.rect(screen, BAR_COLOR,
                               (bar_x, bar_y + 2, visible_width, bar_height - 4))
                pygame.draw.rect(screen, BAR_HIGHLIGHT3,
                               (bar_x, bar_y + 2, visible_width, highlight_height3))
                pygame.draw.rect(screen, BAR_HIGHLIGHT2,
                               (bar_x, bar_y + 2, visible_width, highlight_height2))
                pygame.draw.rect(screen, BAR_HIGHLIGHT1,
                               (bar_x, bar_y + 2, visible_width, highlight_height1))
        elif block_x < bar_x + bar_width:
            visible_width = min(block_width, bar_x + bar_width - block_x)
            pygame.draw.rect(screen, BAR_COLOR,
                           (block_x, bar_y + 2, visible_width, bar_height - 4))
            pygame.draw.rect(screen, BAR_HIGHLIGHT3,
                           (block_x, bar_y + 2, visible_width, highlight_height3))
            pygame.draw.rect(screen, BAR_HIGHLIGHT2,
                           (block_x, bar_y + 2, visible_width, highlight_height2))
            pygame.draw.rect(screen, BAR_HIGHLIGHT1,
                           (block_x, bar_y + 2, visible_width, highlight_height1))

    pygame.display.flip()

pygame.quit()
sys.exit()

if __name__ == "__main__":
    download_coffee_gif()