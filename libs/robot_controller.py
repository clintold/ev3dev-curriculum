"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
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

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """Turns the robot a given amount of degrees at a given speed"""
        self.left_motor.run_to_rel_pos(position_sp=(-degrees_to_turn * 1.44 * math.pi), speed_sp=turn_speed_sp,
                                       stop_action="brake")
        self.right_motor.run_to_rel_pos(position_sp=(degrees_to_turn * 1.44 * math.pi), speed_sp=turn_speed_sp,
                                        stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        """Raises and lowers the arm to figure out the bottom position"""
        assert self.arm_motor.connected
        assert self.touch_sensor

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action='brake')
        ev3.Sound.beep().wait()
        self.arm_motor.run_to_rel_pos(position_sp=-5112)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.arm_motor.position = 0

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

    def shutdown(self):
        """Stops the robot's motors, says goobye, and registers as off"""
        self.running = False
        self.left_motor.stop(stop_action='brake')
        self.right_motor.stop(stop_action='brake')

        ev3.Sound.speak('Goodbye')

    def loop_forever(self):
        """Waits forever for a certain imput"""
        self.running = True
        while self.running:
            time.sleep(0.01)

    def drive_until_otherwise(self, rspeed, lspeed):
        """Turns the robot at a certain speed forever"""
        self.left_motor.run_forever(speed_sp=lspeed)
        self.right_motor.run_forever(speed_sp=rspeed)

    def stop(self):
        """Stops the robot's motors"""
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def seek_beacon(self):
        """The robot seeks out the ir controller's beacon"""
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # Use the beacon_seeker object to get the current heading and distance.
            current_heading = self.seeker.heading  # use the beacon_seeker heading
            current_distance = self.seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) <= 2:
                    if current_distance > 1:
                        # Close enough of a heading to move forward
                        self.left_motor.run_forever(speed_sp=forward_speed)
                        print("On the right heading. Distance: ", current_distance)
                        self.right_motor.run_forever(speed_sp=forward_speed)
                        # You add more!
                    else:
                        print("Found it")
                        time.sleep(1)
                        self.right_motor.stop(stop_action="brake")
                        self.left_motor.stop(stop_action="brake")
                        return True
                elif math.fabs(current_heading) > 10:
                    print("Heading is too far off to fix: ", current_heading)
                    self.left_motor.stop(stop_action="brake")
                    self.right_motor.stop(stop_action="brake")
                    return False
                elif current_heading > 2:
                    print("Adjusting heading: ", current_heading)
                    while current_heading > 2:
                        current_heading = self.seeker.heading  # use the beacon_seeker heading
                        self.right_motor.run_forever(speed_sp=-turn_speed)
                        self.left_motor.run_forever(speed_sp=turn_speed)
                        self.left_motor.stop(stop_action="brake")
                        self.right_motor.stop(stop_action="brake")
                elif current_heading < -2:
                    print("Adjusting heading: ", current_heading)
                    while current_heading < -2:
                        current_heading = self.seeker.heading  # use the beacon_seeker heading
                        self.right_motor.run_forever(speed_sp=turn_speed)
                        self.left_motor.run_forever(speed_sp=-turn_speed)
                        self.left_motor.stop(stop_action="brake")
                        self.right_motor.stop(stop_action="brake")
                else:
                    print("failure")
            time.sleep(0.3)

    def seek_pizza(self, color, speed, finesse, power):
        """The robot seeks out the pizza"""
        ev3.Sound.speak("seeking").wait()

        if color == 'Red':
            self.pixy.mode = "SIG1"
        elif color == 'Blue':
            self.pixy.mode = "SIG5"
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
            #if width > 50.5:
                #self.stop()
                #self.arm_up()
            if self.ir_sensor.proximity < .5:
                self.stop()
                self.arm_up()

            if x < 155:
                self.drive_until_otherwise(turn_speed, -turn_speed)

            else:
                if x > 175:
                    self.drive_until_otherwise(-turn_speed, turn_speed)

                else:
                    self.drive_inches(4, speed)

            time.sleep(0.25)

        ev3.Sound.speak("Pizza probably acquired").wait()

    def seek_destination(self, color, speed):
        """The robot seeks out the pizza"""
        ev3.Sound.speak("destination now")

        if color == 'Red House':
            self.pixy.mode = "SIG1"
        elif color == 'Blue House':
            self.pixy.mode = "SIG5"
        else:
            self.pixy.mode = "SIG3"

        turn_speed = 100

        while True:
            x = self.pixy.value(1)
            y = self.pixy.value(2)
            width = self.pixy.value(3)
            if width > 53:
                self.stop()
                self.arm_down()
                break

            if x < 150:
                self.drive_until_otherwise(turn_speed, -turn_speed)

            else:
                if x > 170:
                    self.drive_until_otherwise(-turn_speed, turn_speed)

                else:
                    self.drive_inches(4, speed)

            time.sleep(0.25)

        ev3.Leds.all_off()
        self.stop()
        ev3.Sound.speak("Pizza Delivered. Mama Mee uh").wait()

    def spirit(self,tone):
        ev3.Sound.tone(tone,3000)