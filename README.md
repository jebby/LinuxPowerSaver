# LinuxPowerSaver

A command line screen dimmer for laptops running Linux using Gnome Shell.

## Features:

- Quit on changing manually changing brightness.

- Custom power profile.

- Change backlight fade in / out speed.

- Update when charging status is changed.

## Requirements:

- A laptop running Linux
- Gnome shell (Only tested on 3.26.2, feel free to try this out and tell me if a past version works!)

## Command line parameters:

- `-v, --verbose` - Run the program in verbose mode. Without this, the program does not output to the shell.

- `-m, --manual` - Don't kill the program if the brightness is manually changed by the user.

- `-f, --fade` - How fast the brightness will fade in or out. Default: .25

- `-t, --time` - The amount of time to wait between polls to the battery (in seconds). Default: 2

- `-p, --profile` - The profile (settings file) used to set brightness values. File must be .json.

## Usage:

- Run the program with default parameters. (Verbose off, Manual off, Fade 0.25, time 2, profile DEFAULT)
`python3 main.py`

- Run the program with shell output.
`python3 main.py -v`

- Kill the program if brightness is manually changed.
`python3 main.py -m`

- Make screen brightness fade in / out faster
`python3 main.py -f .01`

- Increase time between polls
`python3 main.py -t 5`

- Specify a profile (settings file) to use (See **Settings file structure** below)
`python3 main.py -p ~/Documents/my_profile.json`

## Settings file structure:

A settings file `settings.json` is included with this program. The program will use this file by default if the
`-p` or `--profile` arguments are not passed. To define a custom settings file it must have the following:


    {
       "on_battery_brightness": {
         "low": low brightness value while not charging,
        "medium": medium brightness value while not charging,
         "high": high brightness value while not charging
      },
       
      "on_charge_brightness": {
        "low": low brightness value while charging,
        "medium": medium brightness value while charging,
        "high": high brightness value while charging
      },
      
      "levels": {
        "low": [lower range, upper range],
        "medium" :[lower range, upper range],
        "high": [lower range, upper range]
      }
    }
