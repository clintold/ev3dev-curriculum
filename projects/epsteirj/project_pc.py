import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

def main():
    code=2
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title = "Code Window"

    main_frame = ttk.Frame(root, padding=50)
    main_frame.grid()

    box1_label = ttk.Label(main_frame, text="1")
    box1_label.grid(row=0, column=0)
    box1 = ttk.Entry(main_frame, width=4)
    box1.insert(0, "0")
    box1.grid(row=1, column=1)

    return_button = ttk.Button(main_frame, text="enter")
    return_button.grid(row=4, column=(5))
    return_button['command'] = (lambda: check_code(code))

    root.mainloop()

def check_code(code):
    print(code)