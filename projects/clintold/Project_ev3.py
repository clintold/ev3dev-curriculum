import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

def main():
    color_sensor = ev3.ColorSensor()
    btn = ev3.Button()
    robot = robo.Snatch3r()
    robot.arm_calibration()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()
    while not btn.backspace:
        current_color = color_sensor.color
        if current_color == ev3.ColorSensor.COLOR_RED:
            # will add to the red team score
            mqtt_client.send_message("add_red",[])
        if current_color == ev3.ColorSensor.COLOR_BLUE:
            mqtt_client.send_message("add_blue", [])
        mqtt_client.send_message("print_value",[current_color])
        print("current_color", current_color)
    robot.shutdown()


main()
