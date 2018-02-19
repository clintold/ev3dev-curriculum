import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()
    root = tkinter.Tk()
    root.title = "Code Window"

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    for k in range(digits):
        box_label = ttk.Label(main_frame, text=" ")
        box_label.grid(row=1, column=k)
        box = ttk.Entry(main_frame, width=4)
        box.insert(0, "0")
        box.grid(row=2, column=k)

    return_button = ttk.Button(main_frame, text="enter")
    return_button.grid(row=4, column=(digits // 2))
    return_button['command'] = (lambda: check_code(code))