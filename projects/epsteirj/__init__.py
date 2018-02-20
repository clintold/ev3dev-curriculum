
import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com
import time

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

class bot(object):

    def __init__(self):
        self.robot = robo.Snatch3r()
        self.mqtt_client = None
        self.running = True
        self.touch_sensor = ev3.TouchSensor()
        self.seeker = ev3.BeaconSeeker(channel=1)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)

        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()

        self.code=[]

        assert self.color_sensor
        assert self.ir_sensor
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected

    def drive_over_colors(self, digits):
        COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        ev3.Sound.speak("Driving over Colors").wait()
        old_color = 6
        self.code=[]
        while len(self.code) != digits:
            self.drive_until_otherwise(500, 500)
            if self.color_sensor.color != old_color:
                if old_color == 6:
                    old_color = self.color_sensor.color
                    self.code.append(old_color)
                else:
                    old_color = 6
        self.stop()
        while self.running:
            ev3.Sound.speak("starting sequence").wait()
            for k in range(digits):
                ev3.Sound.speak(COLOR_NAMES[self.code[k]]).wait()
                time.sleep(.5)


    def drive_until_otherwise(self, rspeed, lspeed):
        """Turns the robot at a certain speed forever"""
        self.left_motor.run_forever(speed_sp=lspeed)
        self.right_motor.run_forever(speed_sp=rspeed)

    def stop(self):
        """Stops the robot's motors"""
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def loop_forever(self):
        """Waits forever for a certain imput"""
        self.running = True
        while self.running:
            time.sleep(0.01)

def main():
    my_delegate=bot()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_pc()
    my_delegate.loop_forever()
















main()