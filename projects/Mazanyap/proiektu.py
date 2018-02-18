
"""
Author: Alex Mazany.
"""

import ev3dev.ev3 as ev3
import time
import mqtt_remote_method_calls as com
import robot_controller as robo

class orders(object):
    """ Delegate that listens for responses from EV3. """

    def __init__(self):
        self.mqtt_client = None
        self.running = True
        self.touch_sensor = ev3.TouchSensor()
        self.seeker = ev3.BeaconSeeker(channel=1)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)

        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        assert self.pixy
        assert self.color_sensor
        assert self.ir_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected

    def drive_inches(self, inches_target, speed_deg_per_second):
        """Drives the robot forward using the given speeds and distances"""
        self.left_motor.run_to_rel_pos(position_sp=(inches_target * 90), speed_sp=speed_deg_per_second,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=(inches_target * 90), speed_sp=speed_deg_per_second,
                                        stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def drive_until_otherwise(self, rspeed, lspeed):
        """Turns the robot at a certain speed forever"""
        self.left_motor.run_forever(speed_sp=lspeed)
        self.right_motor.run_forever(speed_sp=rspeed)

    def stop(self):
        """Stops the robot's motors"""
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def arm_up(self):
        """Raises the robot's arm"""
        assert self.arm_motor.connected
        assert self.touch_sensor

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Lowers the robot arm to the calibrated 0 position"""
        arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        assert arm_motor.connected

        arm_motor.run_to_abs_pos(position_sp=0)
        arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def seek_pizza(self, pizza, destination, speed, finesse, power):
        print('inmod seek pizza')
        """The robot seeks out the pizza"""
        if pizza == 'Red':
            self.pixy.mode = "SIG2"
        elif pizza == 'Blue':
            self.pixy.mode = "SIG1"
        else:
            self.pixy.mode = "SIG3"

        turn_speed = 100

        if finesse:
            ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.ORANGE)
            ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)

        if power:
            ev3.Sound.speak("AHHHHHHHHHHHHH").wait()

        while not self.touch_sensor.is_pressed:
            x = self.pixy.value(1)
            y = self.pixy.value(2)
            width = self.pixy.value(3)
            if width > 200:
                self.arm_up()

            if x < 150:
                self.drive_until_otherwise(turn_speed, -turn_speed)

            else:
                if x > 170:
                    self.drive_until_otherwise(-turn_speed, turn_speed)

                else:
                    self.drive_inches(15, speed)

            time.sleep(0.25)

        ev3.Sound.speak("Pizza probably acquired").wait()

        if destination == 'Red House':
            self.pixy.mode = "SIG2"
        elif destination == 'Blue House':
            self.pixy.mode = "SIG1"
        else:
            self.pixy.mode = "SIG3"

        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            x = self.pixy.value(1)
            y = self.pixy.value(2)
            width = self.pixy.value(3)
            if width > 200:
                self.arm_down()

            if x < 150:
                self.drive_until_otherwise(turn_speed, -turn_speed)

            else:
                if x > 170:
                    self.drive_until_otherwise(-turn_speed, turn_speed)

                else:
                    self.drive_inches(15, speed)

            time.sleep(0.25)

        ev3.Leds.all_off()
        ev3.Sound.speak("Pizza Delivered. Mama Mia").wait()


    def loop_forever(self):
        """Waits forever for a certain imput"""
        self.running = True
        while self.running:
            time.sleep(0.01)


def main():
    print("--------------------------------------------")
    print(" Pizza Time")
    print("--------------------------------------------")
    ev3.Sound.speak("Pizza delivery").wait()

    robot = robo.Snatch3r()
    robot.arm_calibration()
    mqtt_client = com.MqttClient(robot)
    #my_delegate = orders()
    #mqtt_client = com.MqttClient(my_delegate)
    #my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()

    robot.loop_forever()
# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()