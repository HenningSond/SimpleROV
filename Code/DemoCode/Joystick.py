import pygame

# Initialization of PyGame
Ready = True
pygame.init()
print(pygame.joystick.get_count())
if pygame.joystick.get_count() == 1:
    pygame.display.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(pygame.joystick.get_init())
    while Ready:
        # Get controller readings
        pygame.event.get()

        x = joystick.get_axis(0)
        y = joystick.get_axis(1)
        z = joystick.get_axis(4)
        hat = joystick.get_hat(0)
        print(hat)
        if (pygame.joystick.get_count() != 1):
            print("Joystick disconnected")
            break
else:
    print("No Joystick Available")
