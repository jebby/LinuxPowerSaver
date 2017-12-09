import os
import subprocess
import re


class BrightnessManager:
    '''Used to get and set system brightness on Linux based systems.'''

    def __init__(self):
        self.brightness_regex = re.compile(r'([0-9]*)')

    def set_brightness(self, value):
        '''Make a system call to gdbus to change the screen brightness.
        The value passed in must be a number between 0 - 100.'''

        if not 0 <= value <= 100:
            raise Exception("Brightness value must be between 0 and 100")

        cmd = 'gdbus call --session --dest org.gnome.SettingsDaemon.Power '\
            '--object-path /org/gnome/SettingsDaemon/Power '\
            '--method org.freedesktop.DBus.Properties.Set '\
            'org.gnome.SettingsDaemon.Power.Screen Brightness "<int32 {}>" '\
            '> /dev/null'.format(value)

        os.system(cmd)

    def get_brightness(self):
        '''Make a system call to gdbus and get the system brightness.'''

        cmd = "gdbus call --session --dest org.gnome.SettingsDaemon.Power "\
            "--object-path /org/gnome/SettingsDaemon/Power "\
            "--method org.freedesktop.DBus.Properties.Get "\
            "org.gnome.SettingsDaemon.Power.Screen Brightness"

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        result = self.brightness_regex.findall(proc.stdout.read().decode())
        return int(''.join(result))
