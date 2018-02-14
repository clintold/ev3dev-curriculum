#Epsteirj CS Project

import ev3dev.ev3 as ev3
import time
import robot_controller as robo

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

def main():
    digits=5
    robot = robo.Snatch3r()
    while True:
        command_to_run = input("Whole number value up to ten to set digit count,r (for running code maker, or b (break the code): ")
        if command_to_run == '1':
            digits = 1
            print("Length of code is {}.".format(digits))
        elif command_to_run == '2':
            digits = 2
            print("Length of code is {}.".format(digits))
        elif command_to_run == '3':
            digits = 3
            print("Length of code is {}.".format(digits))
        elif command_to_run == '4':
            digits = 4
            print("Length of code is {}.".format(digits))
        elif command_to_run == '5':
            digits = 5
            print("Length of code is {}.".format(digits))
        elif command_to_run == '6':
            digits = 6
            print("Length of code is {}.".format(digits))
        elif command_to_run == '7':
            digits = 7
            print("Length of code is {}.".format(digits))
        elif command_to_run == '8':
            digits = 8
            print("Length of code is {}.".format(digits))
        elif command_to_run == '9':
            digits = 9
            print("Length of code is {}.".format(digits))
        elif command_to_run == '10':
            digits = 10
            print("Length of code is {}.".format(digits))
        elif command_to_run == 'r':
            print("Start driving over colors")
            drive_over_colors(robot,digits)
        elif command_to_run == 'b':
            print("beginning decoding")

        else:
            print(command_to_run, "is not a known command. Please enter a valid choice.")


def drive_over_colors(robot,digits):
    ev3.Sound.speak("Driving over Colors").wait()
    code_list=[]
    current_color = 6
    while not len(code_list) == digits:
        robot.drive_until_otherwise(500,500)
        if robot.color_sensor.color != current_color:
            if current_color == 6:
                current_color=robot.color_sensor.color
                code_list = code_list + current_color
            if current_color !=6:
                current_color = 6
    robot.stop()
    return code_list























main()