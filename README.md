# Scripts for T208 UPS module

## Limitations
[T208](https://wiki.geekworm.com/T208) is a UPS module for Jetson Nano, powered by 1~6x 18650 batteries. It is mounted directly under the Jetson Nano board, so peeking into this assembley is needed in order to check the indicators on the UPS board. Geekworm, the maker of this board, do support the [python codes](https://wiki.geekworm.com/T208-Software)([GitHub repository](https://github.com/geekworm-com/T208)) so that user can check the status of UPS via I2C and GPIO control, but those are using outdated __Python2__ modules and include some minor bugs. Based on the codes given, I'm trying to build my own script that runs on __Python3__ based modules with some dev-friendly improvements.


## Goal

### ✅ Done
- Replace Python2 with **Python3**
  - Codes in `python` folder.
- **JSON**-style output support
  - `python/t208_report.py`

### 🔜 Ongoing
- Polish codes
  - Help(something like `--help`) messages
  - Add some descriptions in completed codes
- Audible alert via GPIO control
- Battery level ROS publisher node

### 🛑 Unclear to be done, but considering
- Desktop notification integration (mainly for ~~LXDE~~ LXQt)
- Integrate UPS battery level with ubuntu battery management system, so that indicator can show remaining battery level.
- Automatic performance(power comsumption) mode adjustment based on battery level
- Automatic shutdown when battery level critical


## Supported system version of Jetson Nano

- Latest official Jetpack (Ubuntu 18.04)
