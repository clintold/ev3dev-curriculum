import mqtt_remote_method_calls as com
import robot_controller as robo
import ev3dev.ev3 as ev3

def main():
    color_sensor = ev3.ColorSensor()
    current_color = color_sensor.color
    btn = ev3.Button()
    robot = robo.Snatch3r()
    robot.arm_calibration()
    while not btn.backspace:

        mqtt_client = com.MqttClient(robot)
        mqtt_client.connect_to_pc()
        if current_color == ev3.ColorSensor.COLOR_RED:
            # will add to the red team score
            mqtt_client.send_message("add_red",[])
        if current_color == ev3.ColorSensor.COLOR_BLUE:
            mqtt_client.send_message("add_blue", [])

    robot.shutdown()