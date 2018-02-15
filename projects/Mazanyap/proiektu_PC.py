import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()



    root = tkinter.Tk()
    root.title("Delivery Mainframe")

    main_frame = ttk.Frame(root, padding=50)
    main_frame.grid()

    radio_frame = ttk.Frame(main_frame, borderwidth=5, relief='raised')
    radio_frame1 = ttk.Frame(main_frame, borderwidth=5, relief='raised')
    button_frame = ttk.Frame(main_frame, borderwidth=5, relief='raised')
    checkbox_frame = ttk.Frame(main_frame, borderwidth=5, relief='raised')
    radio_frame.grid(sticky='w')
    radio_frame1.grid(sticky='w')
    button_frame.grid(sticky='w')
    checkbox_frame.grid(sticky='w')

    pizza_color_label = ttk.Label(radio_frame, text="Type of Pizza")
    pizza_color_label.grid(row=0, column=0)
    pizza_color_button = ttk.Radiobutton(radio_frame, text='Red', variable='btn1', value=1)
    pizza_color_button.grid(row=1, column=0)
    pizza_color_button.grid(sticky='w')

    pizza_color_button2 = ttk.Radiobutton(radio_frame, text='Blue', variable='btn1', value=2)
    pizza_color_button2.grid(row=2, column=0)
    pizza_color_button2.grid(sticky='w')

    pizza_color_button3 = ttk.Radiobutton(radio_frame, text='Green', variable='btn1', value=3)
    pizza_color_button3.grid(row=3, column=0)
    pizza_color_button3.grid(sticky='w')

    pizza_destination_label = ttk.Label(radio_frame1, text="Destination")
    pizza_destination_label.grid(row=0, column=2)
    pizza_destination_button1 = ttk.Radiobutton(radio_frame1, text='Red House', variable='btn2', value=4,)
    pizza_destination_button1.grid(row=1, column=2)
    pizza_destination_button1.grid(sticky='w')

    pizza_destination_button2 = ttk.Radiobutton(radio_frame1, text='Blue House', variable='btn2', value=5)
    pizza_destination_button2.grid(row=2, column=2)
    pizza_destination_button2.grid(sticky='w')

    pizza_destination_button3 = ttk.Radiobutton(radio_frame1, text='Green House', variable='btn2', value=6)
    pizza_destination_button3.grid(row=3, column=2)
    pizza_destination_button3.grid(sticky='w')

    checkbox_label = ttk.Label(checkbox_frame, text="Modes")
    checkbox_label.grid(row=0, column=0)
    power_mode = ttk.Checkbutton(checkbox_frame, text='Power Mode')
    power_mode.grid(row=1, column=0)

    speed_mode = ttk.Checkbutton(checkbox_frame, text='Speed Mode')
    speed_mode.grid(row=2, column=0)

    finesse_mode = ttk.Checkbutton(checkbox_frame, text='Finesse Mode')
    finesse_mode.grid(row=3, column=0)

    power_mode_observer = tkinter.StringVar()
    power_mode['variable'] = power_mode_observer

    speed_mode_observer = tkinter.StringVar()
    speed_mode['variable'] = speed_mode_observer

    finesse_mode_observer = tkinter.StringVar()
    finesse_mode['variable'] = finesse_mode_observer

    power_mode['command'] = lambda: power_mode_state(power_mode_observer)
    speed_mode['command'] = lambda: speed_mode_state(speed_mode_observer)
    finesse_mode['command'] = lambda: finesse_mode_state(finesse_mode_observer)

    # Buttons for quit and exit
    a_button = ttk.Button(button_frame, text="Activate")
    a_button.grid(row=4, column=2)
    a_button['command'] = ()

    q_button = ttk.Button(button_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(button_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    c = 0
    for widget in [radio_frame, radio_frame1, checkbox_frame, button_frame]:
        widget.grid(row=0, column=c, padx=10)
        c = c + 1

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------
# Done: 4. Implement the functions for the drive button callbacks.

# Done: 5. Call over a TA or instructor to sign your team's checkoff sheet and do a code review.  This is the final one!
#
# Observations you should make, you did basically this same program using the IR Remote, but your computer can be a
# remote control that can do A LOT more than an IR Remote.  We are just doing the basics here.


def power_mode_state(power_mode_observer):
    if power_mode_observer.get():
        print('Power mode')


def speed_mode_state(speed_mode_observer):
    if speed_mode_observer.get():
        print('Speed mode')


def finesse_mode_state(finesse_mode_observer):
    if finesse_mode_observer.get():
        print('Finesse mode')


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


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
