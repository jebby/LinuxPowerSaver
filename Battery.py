import os
import subprocess

class Battery:
    '''A basic wrapper around the files in
    /sys/class/power_supply/BAT0 in Linux to get
    battery percent and charging status on a laptop.'''

    def __init__(self):
        if not os.path.exists("/sys/class/power_supply/BAT0"):
            raise Exception("No Battery Present")

    def percent(self):
        return int(self.get("capacity"))

    def is_charging(self):
        status = self.get("status")
        return status != "Discharging"

    def get(self, file):
        f = os.path.join("/sys/class/power_supply/BAT0", file)

        cmd = "cat {}".format(f)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        result = proc.stdout.read().decode().split("\n")[0]
        proc.stdout.close()

        return result