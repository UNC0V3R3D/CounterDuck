# CounterDuck
<img src="https://github.com/UNC0V3R3D/ressources/blob/main/counterduck_gradient.png" height="420" width="1200" >

CounterDuck is a Python program designed to prevent BadUSB attacks. This program helps protect against malicious USB devices by constantly monitoring and blocking suspicious USB activity. With CounterDuck, you can protect your computer and personal information from potentially harmful USB devices.

## Installation

Follow the instructions below.

```bash
git clone https://github.com/UNC0V3R3D/CounterDuck.git
```

## Usage

```
1. (In CMD) "pip install -r requirements.txt"
2. Run setup.py
3. The script will be put into the autostart folder of Windows.
4. Restart your PC.
5. Ready to go, everytime you start your pc the script is automatically activated.
```
## Features

The script has multiple features, here is a quick list:

- Search USB devices for common serial ids like "flip" for the Flipper Zero
- Disconnect any new USB device that connects
- Block keyboard input if keys have been pressed too fast
- Hide process and randomly name it

## Future

Of course I will be working on this and there will be many new features coming.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.


## License

[MIT](https://choosealicense.com/licenses/mit/)
