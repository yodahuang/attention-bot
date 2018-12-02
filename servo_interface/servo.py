import argparse

import wiringpi


class Servo:
    def __init__(self):
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(1, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

        # divide down clock
        wiringpi.pwmSetClock(192)
        wiringpi.pwmSetRange(2000)

    def go(self, angle):
        if angle < 0:
            angle = 0
        if angle > 180:
            angle = 180
        pwm_value = int(191 / 180 * angle + 50)
        wiringpi.pwmWrite(1, pwm_value)


def main():

    parser = argparse.ArgumentParser(description='Just pwm it')
    parser.add_argument('--angle', type=int, help='An angle between 0 and 180')
    args = parser.parse_args()

    servo = Servo()
    servo.go(args.angle)

if __name__ == '__main__':
    main()
