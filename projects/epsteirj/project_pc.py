import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

def main():
    digits = 5
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    while True:
        command_to_run = input("Whole number value up to ten, r (for running), or b (break the code): ")
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
            code_input=drive_over_colors(robot,digits)
        elif command_to_run == 'b':
            print("beginning decoding")
            display_code(code_input)
        else:
            print(command_to_run, "is not a known command. Please enter a valid choice.")

def main():
    code=2
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title = "Code Window"

    main_frame = ttk.Frame(root, padding=50)
    main_frame.grid()

    box1_label = ttk.Label(main_frame, text=" ")
    box1_label.grid(row=0, column=0)
    box1 = ttk.Entry(main_frame, width=4)
    box1.insert(0, "0")
    box1.grid(row=1, column=0)

    box2_label = ttk.Label(main_frame, text=" ")
    box2_label.grid(row=0, column=1)
    box2 = ttk.Entry(main_frame, width=4)
    box2.insert(0, "0")
    box2.grid(row=1, column=2)

    box3_label = ttk.Label(main_frame, text=" ")
    box3_label.grid(row=0, column=3)
    box3 = ttk.Entry(main_frame, width=4)
    box3.insert(0, "0")
    box3.grid(row=1, column=4)

    box4_label = ttk.Label(main_frame, text=" ")
    box4_label.grid(row=0, column=5)
    box4 = ttk.Entry(main_frame, width=4)
    box4.insert(0, "0")
    box4.grid(row=1, column=6)

    box5_label = ttk.Label(main_frame, text=" ")
    box5_label.grid(row=0, column=7)
    box5 = ttk.Entry(main_frame, width=4)
    box5.insert(0, "0")
    box5.grid(row=1, column=8)

    box6_label = ttk.Label(main_frame, text=" ")
    box6_label.grid(row=0, column=9)
    box6 = ttk.Entry(main_frame, width=4)
    box6.insert(0, "0")
    box6.grid(row=1, column=10)

    box7_label = ttk.Label(main_frame, text=" ")
    box7_label.grid(row=0, column=11)
    box7 = ttk.Entry(main_frame, width=4)
    box7.insert(0, "0")
    box7.grid(row=1, column=12)

    box8_label = ttk.Label(main_frame, text=" ")
    box8_label.grid(row=0, column=13)
    box8 = ttk.Entry(main_frame, width=4)
    box8.insert(0, "0")
    box8.grid(row=1, column=14)

    box9_label = ttk.Label(main_frame, text=" ")
    box9_label.grid(row=0, column=15)
    box9 = ttk.Entry(main_frame, width=4)
    box9.insert(0, "0")
    box9.grid(row=1, column=16)

    box10_label = ttk.Label(main_frame, text=" ")
    box10_label.grid(row=0, column=17)
    box10 = ttk.Entry(main_frame, width=4)
    box10.insert(0, "0")
    box10.grid(row=1, column=18)

    spacing_label = ttk.Label(main_frame, text=" ")
    spacing_label.grid(row=2, column=9)

    return_button = ttk.Button(main_frame, text="enter")
    return_button.grid(row=4, column=(9))
    return_button['command'] = (lambda: check_code(box1.get()))

    root.mainloop()

def check_code(box1):
    print(box1)


main()