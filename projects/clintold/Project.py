'''This is the final project for Lucas Clinton in the Winter quarter 2017-2918 class of CSSE120.
  All barrowed code belongs to the individual writers. MAny of thos writers are in the CS and ECE departments.
  Chief writer of borrowed code is David Fisher.
  Author of the program and this project is Luke Clinton'''

import ev3dev.ev3 as ev3
import time
import tkinter
from tkinter import ttk
from tkinter import *


import robot_controller as robo

import mqtt_remote_method_calls as com

def main():
    # Setting up client and connecting to PC
    robot = robo.Snatch3r

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("The Ohio State")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    spirit_label = ttk.Label(main_frame,text="Fighting Spirit!")
    spirit_label.grid(row=8,column=1)
    spirit = Scale(main_frame, from_=0, to=5000, orient=HORIZONTAL)
    spirit.grid(row=7, column=1)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: move(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Up>', lambda event: move(mqtt_client, int(left_speed_entry.get()), int(right_speed_entry.get())))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: move(mqtt_client, -int(left_speed_entry.get()), int(right_speed_entry.get()))
    root.bind('<Left>', lambda event: move(mqtt_client, -int(left_speed_entry.get()), int(right_speed_entry.get())))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: move(mqtt_client, int(left_speed_entry.get()), -int(right_speed_entry.get()))
    root.bind('<Right>', lambda event: move(mqtt_client, int(left_speed_entry.get()), -int(right_speed_entry.get())))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: move(mqtt_client, -int(left_speed_entry.get()), -int(right_speed_entry.get()))
    root.bind('<Down>', lambda event: move(mqtt_client, -int(left_speed_entry.get()), -int(right_speed_entry.get())))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    update_button = ttk.Button(main_frame, text='Renew Spirit')
    update_button.grid(row=10,column=1)
    update_button['command'] = (lambda: update_spirit(mqtt_client, spirit.get()))

    # color_sensor = ev3.ColorSensor()
    # current_color = color_sensor.color
    red_score = 0

    # if current_color == ev3.ColorSensor.COLOR_RED:
    #     # will add to the red team score
    #     red_score = red_score + 1

    spirit_value = spirit.get()

    class MyDelegate:
        def __init__(self):
            self.red_score = 0
            self.blue_score = 0

        def add_red(self):
            self.red_score = self.red_score + 1
            red_score_label = ttk.Label(main_frame, text="Red")
            red_score_label.grid(row=9, column=2)
            red_score_score = ttk.Label(main_frame, text=self.red_score)
            red_score_score.grid(row=10, column=2)

        def add_blue(self):
            self.blue_score = self.blue_score + 1
            blue_score_label = ttk.Label(main_frame, text="Blue")
            blue_score_label.grid(row=9, column=0)
            blue_score_score = ttk.Label(main_frame, text=self.blue_score)
            blue_score_score.grid(row=10, column=0)




    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# Done: 4. Implement the functions for the drive button callbacks.

# Done: 5. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.  This is the final one!
#
# Observations you should make, you did basically this same program using the IR Remote, but your computer can be a
# remote control that can do A LOT more than an IR Remote.  We are just doing the basics here.


# Arm command callbacks
def send_up(mqtt_client):
    print("arm_up")
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    print("arm_down")
    mqtt_client.send_message("arm_down")


def move(mqtt_client, left_speed ,right_speed):
    print('move')
    mqtt_client.send_message("drive_until_otherwise", [right_speed, left_speed])


def stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def update_spirit(mqtt_client,spirit_value):
    mqtt_client.send_message("spirit", [spirit_value])
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
