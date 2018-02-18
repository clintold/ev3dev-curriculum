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
    pizza_color_button = ttk.Radiobutton(radio_frame, text='Red', variable='btn1', value='Red')
    pizza_color_button.grid(row=1, column=0)
    pizza_color_button.grid(sticky='w')

    pizza_color_button2 = ttk.Radiobutton(radio_frame, text='Blue', variable='btn1', value='Blue')
    pizza_color_button2.grid(row=2, column=0)
    pizza_color_button2.grid(sticky='w')

    pizza_color_button3 = ttk.Radiobutton(radio_frame, text='Green', variable='btn1', value='Green')
    pizza_color_button3.grid(row=3, column=0)
    pizza_color_button3.grid(sticky='w')

    pizza_destination_label = ttk.Label(radio_frame1, text="Destination")
    pizza_destination_label.grid(row=0, column=2)
    pizza_destination_button1 = ttk.Radiobutton(radio_frame1, text='Red House', variable='btn2', value='Red House')
    pizza_destination_button1.grid(row=1, column=2)
    pizza_destination_button1.grid(sticky='w')

    pizza_destination_button2 = ttk.Radiobutton(radio_frame1, text='Blue House', variable='btn2', value='Blue House')
    pizza_destination_button2.grid(row=2, column=2)
    pizza_destination_button2.grid(sticky='w')

    pizza_destination_button3 = ttk.Radiobutton(radio_frame1, text='Green House', variable='btn2', value='Green House')
    pizza_destination_button3.grid(row=3, column=2)
    pizza_destination_button3.grid(sticky='w')

    pizza_observer = tkinter.StringVar()
    for radio in [pizza_color_button, pizza_color_button2, pizza_color_button3]:
        radio['variable'] = pizza_observer  # They all need the SAME observer

    destination_observer = tkinter.StringVar()
    for radio in [pizza_destination_button1, pizza_destination_button2, pizza_destination_button3]:
        radio['variable'] = destination_observer  # They all need the SAME observer

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
    a_button['command'] = (lambda: activate_program(mqtt_client, pizza_observer.get(), destination_observer.get(),
                                                    power_mode_observer.get(),speed_mode_observer.get(),
                                                    finesse_mode_observer.get()))

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
    if power_mode_observer.get() == '1':
        print('Power mode activated')


def speed_mode_state(speed_mode_observer):
    if speed_mode_observer.get() == '1':
        print('Speed mode activated')


def finesse_mode_state(finesse_mode_observer):
    if finesse_mode_observer.get() == '1':
        print('Finesse mode activated')


def activate_program(mqtt_client, pizza, destination, power_mode, speed_mode, finesse_mode):
    print('beginning delivery')
    if finesse_mode == '1':
        print('Finesse mode active')
        finesse_state = 1
    else:
        finesse_state = 0

    if speed_mode == '1':
        print('Speed mode active')
        speed = 800
    else:
        speed = 500

    if power_mode == '1':
        print('Power mode active')
        power_state = 1
    else:
        power_state = 0

    print(pizza, 'pizza being delivered to', destination)

    mqtt_client.send_message("seek_pizza", [pizza, speed, finesse_state, power_state])
    mqtt_client.send_message("seek_destination", [destination, speed])



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
