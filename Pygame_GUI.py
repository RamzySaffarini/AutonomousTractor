import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

pygame.init() #initializer

pygame.display.set_caption('Jacob & Ramzy\'s Autonomous Tractor!') # Sets caption at top of window
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FEFFED'))

#Creating "GUI MANAGER"
manager = pygame_gui.UIManager((800, 600), 'theme.json')

# Creating Start button
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((125, 50), (200, 100)),
                                             text='START',
                                             manager=manager, object_id=ObjectID(class_id='@buttons',
                                           object_id='#start_button'))
stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 50), (200, 100)),
                                             text='STOP',
                                             manager=manager, object_id=ObjectID(class_id='@buttons',
                                           object_id='#stop_button'))

clock = pygame.time.Clock()
is_running = True

#allows interactiveness, loops indefinitely
while is_running:
    time_delta = clock.tick(60)/1000.0 #Updates clock each run
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Stops  program if game is quit
            is_running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                  print('STARTING!!!!!!')
            if event.ui_element == stop_button:
                  print('STOPPING!!!!!!')
        manager.process_events(event) # Checks for updates such as clicking

    manager.update(time_delta)

    window_surface.blit(background, (0, 0)) #refreshes page as changes happen so it is not constantly refreshing
    manager.draw_ui(window_surface) #draws UI so user can actually see it

    pygame.display.update()