"""Module for keeping track of and detecting collisions."""

from itertools import product
import sound


def detect_collision(object1, object2):
    """Detects whether a collision has been made between two objects.
    
    Assumes both objects are circles and have x, y and radius attributes."""

    x_dist = object1.x - object2.x
    y_dist = object1.y - object2.y

    total_radius = object1.radius + object2.radius
    return (x_dist * x_dist + y_dist * y_dist) < (total_radius * total_radius)


def detect_eye_asteroid_collisions(eyes, asteroid_class):
    """Iterate between the asteroids to detect collisions between the ship's EYES and asteroids."""
    # test_cases = ((ship, asteroid) for asteroid in asteroid_class.asteroids)
    test_cases = ( (eye, asteroid) for eye in eyes for asteroid in asteroid_class.asteroids )
    # this will result in:  ( (x,1), (x,2), (x,3), (y,1), (y,2), (y,3) ) given lists [x,y] and [1,2,3]
    # return any((detect_collision(*test_case) for test_case in test_cases)) # this is the old method. wont work
    for obj1, obj2 in test_cases:

        delta_x = obj1.x - obj2.x
        delta_y = obj1.y - obj2.y
        rad = obj1.radius + obj2.radius

        straight_line_dist = delta_x*delta_x + delta_y*delta_y
        # print()
        if straight_line_dist - rad < 4000: #magnitude of line
            return (True, obj1) #return what eye is getting dicked
    
    return False


def detect_ship_asteroid_collisions(ship, asteroid_class):
    """Iterate between the asteroids to detect collisions between the ship and asteroids."""
    test_cases = ((ship, asteroid) for asteroid in asteroid_class.asteroids)
    return any((detect_collision(*test_case) for test_case in test_cases))


def return_first_match(element, lst, test):
    """Helper function to find the first match in a list based on a custom test."""
    for i in lst:
        if test(element, i):
            return i


def detect_bullet_asteroid_collisions(bullet_class, asteroid_class):
    """Detect collisions between bullets and asteroids.

    For each asteroid, search through bullets for a collision. If there
    is, delete both the asteroid and the bullet."""

    asteroid_destroy_list = []
    for asteroid in asteroid_class.asteroids.copy():
        bullet = return_first_match(asteroid, bullet_class.bullets, detect_collision)
        if bullet:
            bullet.destroy()
            asteroid.destroy()
            sound.hit()
