import pygame

# init screen
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("color the map")

running = True

def main():
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()
    pygame.quit()