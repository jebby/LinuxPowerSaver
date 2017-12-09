import os
import time

from Settings import Settings
from BrightnessManager import BrightnessManager
from Battery import Battery


class PowerSaver:
    def __init__(self, args=None):
        self.setup(args)

    def setup(self, args=None):
        '''Set up arguments to be used, and initialize Battery and Brightness mangager.'''

        arguments = {
            "verbose": True,
            "manual": False,
            "fade": .25,
            "time": 2,
            "profile": None
        }

        if args is not None:
            for arg in args.keys():
                if arg in arguments:
                    arguments[arg] = args[arg]

        self.arguments = arguments

        if self.arguments["verbose"]:
            print("Arguments", flush=True)
            print("=====================")
            for key, value in self.arguments.items():
                print(key, ":", value, flush=True)
            print("=====================\n")

        self.brightness_manager = BrightnessManager()
        self.battery = Battery()

        self.brightness = self.brightness_manager.get_brightness()
        

        self.charging = self.battery.is_charging()
        self.percent = self.battery.percent()

        self.level = None
        self.min_percent = None
        self.max_percent = None

        if self.arguments["profile"] is None:
            cur_dir = os.path.abspath(os.path.dirname(__file__))
            if self.arguments["verbose"]:
                print("Default settings loaded", flush=True)
            self.settings = Settings(os.path.join(cur_dir, "settings.json"))

        else:
            self.settings = Settings(arguments["profile"])

    def poll(self):
        '''Poll the battery and brightness. If the battery level defined in settings
        has changed, update the screen brightness.'''

        poll_time = self.arguments["time"]

        while True:
            time.sleep(poll_time)
            update = False

            # Get percent, charge status, and brightness
            self.percent = self.battery.percent()
            charging = self.battery.is_charging()
            brightness = self.brightness_manager.get_brightness()

            # Close the program if the brightness
            # was changed manually and not set in
            # command line args.
            if brightness != self.brightness:
                if not self.arguments["manual"]:
                    if self.arguments["verbose"]:
                        print("Brightness Manually Changed, Exiting")
                    exit(1)

            # If the battery level ("low", "medium", "high") is None,
            # then initialize it. and set the brightness to the
            # brightness value corresponding to the level
            # of the battery's percent is currently at
            if self.level is None:
                if self.arguments["verbose"]:
                    print("Battery Level Initializing.", flush=True)
                update = True

            # If the battery percent has moved out of the range of the
            # battery level, then update to change the brightness.
            elif self.percent not in range(self.min_percent, self.max_percent + 1):
                if self.arguments["verbose"]:
                    print("Battery level changed.", flush=True)
                update = True

            # If the battery's charging status has changed,
            # determine if the screen should brighten for charging
            # or dim for discharging.
            elif charging != self.charging:
                if self.arguments["verbose"]:
                    print("Charging status changed:", charging, flush=True)
                update = True

            # Print out the battery percent if verbose was set.
            if self.arguments["verbose"]:
                print(self.percent, flush=True)

            # Only update the brightness if one of the
            # above requirements are met.
            if update:

                self.charging = charging

                # Check what level the battery percent is ("low", "medium", "high")
                # and cache the range that level is in.
                for battery_level, battery_range in self.settings.contents["levels"].items():

                    # If the current percent of the battery is in the range specified in the
                    # battery level, then that is the level needed to get brightness values.
                    if self.percent in range(battery_range[0], battery_range[1] + 1):
                        self.level = battery_level
                        self.min_percent, self.max_percent = battery_range
                        if self.arguments["verbose"]:
                            print("Battery Level: ", self.level, flush=True)
                        break


                # If the battery is charging, handle brightness settings
                # for charging in the settings file.
                if self.charging:
                    target_brightness = self.settings.contents["on_charge_brightness"][self.level]
                    if target_brightness != self.brightness:
                        if target_brightness < self.brightness:
                            levels = reversed(range(target_brightness, self.brightness + 1))
                        else:
                            levels = range(self.brightness, target_brightness + 1)

                        for brightness_level in levels:
                            self.brightness_manager.set_brightness(brightness_level)
                            if self.arguments["verbose"]:
                                print("Setting Brightness:", brightness_level, flush=True)
                            time.sleep(self.arguments["fade"])

                # Otherwise, handle brightness settings
                # for battery usage in the settings file
                else:
                    target_brightness = self.settings.contents["on_battery_brightness"][self.level]
                    if target_brightness != self.brightness:
                        if target_brightness < self.brightness:
                            levels = reversed(range(target_brightness, self.brightness + 1))
                        else:
                            levels = range(self.brightness, target_brightness + 1)

                        for brightness_level in levels:
                            self.brightness_manager.set_brightness(brightness_level)
                            if self.arguments["verbose"]:
                                print("Setting Brightness:", brightness_level, flush=True)
                            time.sleep(self.arguments["fade"])

            # Get the brightness after everything has changed.
            self.brightness = self.brightness_manager.get_brightness()

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-v",
        "--verbose",
        help="Display messages in the terminal each time the battery is polled.\n"
        "Default: On",
        action="store_true"
    )

    parser.add_argument(
        "-m",
        "--manual",
        help="Keep the program open if the brightness is manually changed.\n"
        "Default: Off",
        action="store_true"
    )

    parser.add_argument(
        "-f",
        "--fade",
        help="The speed to fade the brightness in or out.\n"
        "Higher is slower. Default: .25",
        type=float,
        default=.25
    )

    parser.add_argument(
        "-t",
        "--time",
        help="The time to sleep between each poll on the battery. (in seconds)\n"
        "Default: 2",
        type=float,
        default=2
        )

    parser.add_argument(
        "-p",
        "--profile",
        help="The json file to use for battery levels and percentages.",
        type=str
    )

    args = parser.parse_args()

    arguments = {
        "verbose": args.verbose,
        "manual": args.manual,
        "fade": args.fade,
        "time": args.time,
        "profile": None if not args.profile else args.profile,
    }

    powersaver = PowerSaver(arguments)
    powersaver.poll()
