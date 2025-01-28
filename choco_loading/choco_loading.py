import pygame
import sys
from pygame import gfxdraw
import os
import requests

# Start pygame voor het laadscherm
pygame.init()
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 350 
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Downloading...")

# Laadscherm tekst
font = pygame.font.SysFont('arial', 24)
loading_text = font.render("Bestanden worden gedownload...", True, (0, 0, 0))
loading_rect = loading_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

# Toon laadscherm
screen.fill((236, 233, 216))
screen.blit(loading_text, loading_rect)
pygame.display.flip()

def download_image(url, filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    
    if not os.path.exists(file_path):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Afbeelding {filename} succesvol gedownload")
        except Exception as e:
            print(f"Fout bij downloaden van {filename}: {e}")
            return False
    else:
        print(f"Afbeelding {filename} bestaat al")
    return True

images = {
    'item_frame.png': 'https://www.dropbox.com/scl/fi/9egwzfccmmo7i8tsae5j9/item_frame.png?rlkey=84b27e3t7wbes1auki0a4wb6m&st=meq0xrzj&dl=1',
    'choco.png': 'https://www.dropbox.com/scl/fi/8qxd6jwgq6cot33hoipub/choco.png?rlkey=0lpenqhixekplof8b6ltoezcy&st=8pxom9mt&dl=1'
}

# Download alle afbeeldingen eerst
all_images_downloaded = all(download_image(url, filename) for filename, url in images.items())

if not all_images_downloaded:
    error_text = font.render("Fout bij het downloaden. Programma wordt afgesloten.", True, (255, 0, 0))
    error_rect = error_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
    screen.blit(error_text, error_rect)
    pygame.display.flip()
    pygame.time.wait(2000)  # Wacht 2 seconden zodat de gebruiker de foutmelding kan lezen
    pygame.quit()
    sys.exit(1)

# Verander de titel en laad de hoofdafbeeldingen
pygame.display.set_caption("Installing Choco ... ")

font = pygame.font.SysFont('arial', 36, bold=True)
title_text = font.render("Choco wordt geïnstalleerd", True, (0, 0, 0))
title_x = (WINDOW_WIDTH - title_text.get_width()) // 2
title_y = 10

# Gebruik het volledige pad voor het laden van de afbeeldingen
current_dir = os.path.dirname(os.path.abspath(__file__))
frame_path = os.path.join(current_dir, "item_frame.png")
choco_path = os.path.join(current_dir, "choco.png")

frame_image = pygame.image.load(frame_path)
choco_image = pygame.image.load(choco_path)

frame_size = (220, 220)
choco_size = (150, 150)
frame_image = pygame.transform.scale(frame_image, frame_size)
choco_image = pygame.transform.scale(choco_image, choco_size)

frame_x = (WINDOW_WIDTH - frame_image.get_width()) // 2
frame_y = title_y + title_text.get_height() + 10

choco_x = (WINDOW_WIDTH - choco_size[0]) // 2
choco_y = frame_y + (frame_size[1] - choco_size[1]) // 2

BACKGROUND = (236, 233, 216)
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

rotation_angle = 0
rotating = False
target_angle = 0

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            choco_rect = choco_image.get_rect(topleft=(choco_x, choco_y))
            if choco_rect.collidepoint(mouse_x, mouse_y):
                target_angle -= 45
                rotating = True

    screen.fill(BACKGROUND)
    
    screen.blit(title_text, (title_x, title_y))
    
    if rotating:
        if rotation_angle > target_angle:
            rotation_angle -= 5
            if rotation_angle <= target_angle:
                rotation_angle = target_angle
                rotating = False

    rotated_choco = pygame.transform.rotate(choco_image, rotation_angle)
    rotated_rect = rotated_choco.get_rect(center=(choco_x + choco_size[0]//2, choco_y + choco_size[1]//2))
    screen.blit(frame_image, (frame_x, frame_y))
    screen.blit(rotated_choco, rotated_rect.topleft)

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
    clock.tick(60)

pygame.quit()
sys.exit()
