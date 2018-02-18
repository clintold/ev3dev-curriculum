
"""
Author: Alex Mazany.
"""

import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com
import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Pizza Time")
    print("--------------------------------------------")
    ev3.Sound.speak("Pizza delivery").wait()

    robot = robo.Snatch3r()
    robot.arm_calibration()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    robot.loop_forever()
    robot.stop()
    print("Pizza Delivered!")
    ev3.Sound.speak("Mama Mia").wait()

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()