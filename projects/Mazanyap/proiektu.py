
"""
Author: Alex Mazany.
"""

import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Pizza Time")
    print("--------------------------------------------")
    ev3.Sound.speak("Pizza delivery").wait()

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    turn_speed = 100

    x = robot.pixy.value(1)
    y = robot.pixy.value(2)

    print("(X, Y) = ({}, {})".format(x, y))


    if x < 150:
        robot.drive_until_otherwise(turn_speed, -turn_speed)

    else:
        if x > 170:
            robot.drive_until_otherwise(-turn_speed, turn_speed)

        else:
            robot.stop()

        time.sleep(0.25)

    robot.stop()
    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()