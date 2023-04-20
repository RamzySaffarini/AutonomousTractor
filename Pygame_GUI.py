import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

import asyncio
from bleak import BleakClient

address = "a0:6c:65:cf:9e:0e" #MAC
MODEL_NBR_UUID = "0000FFE1-0000-1000-8000-00805F9B34FB" #UUID
numTapesCrossed = 0


pygame.init() #initializer

pygame.display.set_caption('Jacob & Ramzy\'s Autonomous Tractor!') # Sets caption at top of window
window_surface = pygame.display.set_mode((800, 600)) #Creates 800x600 window

background = pygame.Surface((800, 600)) #creates window background of 800x600
background.fill(pygame.Color('#ADD8E6')) #Makes it into cream color

#Creating "GUI MANAGER" which handles try/except clauses, etc. Imports json file dictating themes
manager = pygame_gui.UIManager((800, 600), 'theme.json') 

# Creating Start button
start_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((200, 50), (200, 100)),
                                             text='START',
                                             manager=manager, object_id=ObjectID(class_id='@buttons',
                                           object_id='#start_button'))
stop_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 50), (200, 100)),
                                             text='STOP',
                                             manager=manager, object_id=ObjectID(class_id='@buttons',
                                           object_id='#stop_button'))
trip_report = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500, 200), (200, 100)),
                                             text='GENERATE TRIP REPORT',
                                             manager=manager, object_id=ObjectID(class_id='@buttons',
                                           object_id='#trip_report'))
time_elapsed = pygame_gui.elements.UITextBox("<b>Time Elapsed:</b> 00:00",
                                        relative_rect=pygame.Rect((200, 200), (200, 50)),
                                        manager=manager)
tapes_crossed = pygame_gui.elements.UITextBox("<b>Tapes Crossed: </b>" + str(numTapesCrossed),
                                        relative_rect=pygame.Rect((200, 250), (200, 50)),
                                        manager=manager)

clock = pygame.time.Clock()
is_running = True #initialize boolean for indefinite loop
def callback(sender: address, data: bytearray):
    print(f"{data}")
    # if receives indication that numtapes increases
    # numTapesCrossed += 1
def generateTripReport():
   pass

#places into main async i/o function to be called
async def main():
    async with BleakClient(address) as client:
        
        #allows interactiveness, loops indefinitely
        global is_running #allows global variable to be accessed
        global numTapesCrossed
        while is_running: #indefinite loop
            time_delta = clock.tick(60)/1000.0 #Updates clock each run
            for event in pygame.event.get(): #returns if there is an event ()
                if event.type == pygame.QUIT: #Stops  program if game is quit
                    is_running = False #stops program
                if event.type == pygame_gui.UI_BUTTON_PRESSED: # If a button is pressed
                    if event.ui_element == start_button: #If button pressed was the start button
                        #   print('STARTING!!!!!!') #for debugging purposes
                          await client.write_gatt_char(MODEL_NBR_UUID, b'g') #sends the go signal to Arduino
                    if event.ui_element == stop_button: #If button pressed was stop
                        #   print('STOPPING!!!!!!') #for debugging purposes
                          await client.write_gatt_char(MODEL_NBR_UUID, b's') #sends stop signal to Arduino                 
                    if event.ui_element == trip_report:
                         await client.start_notify(MODEL_NBR_UUID, callback)
                         await asyncio.sleep(5.0)
                         await client.stop_notify(MODEL_NBR_UUID)
                
                manager.process_events(event) # Checks for updates such as clicking

            manager.update(time_delta) #adjusts theme based on user interaction, like hovering over buttons

            window_surface.blit(background, (0, 0)) #refreshes page as changes happen so it is not constantly refreshing
            manager.draw_ui(window_surface) #draws UI so user can actually see it

            pygame.display.update() #actually impacts the display so user can see
            
asyncio.run(main()) #runs async  i/o loop


     