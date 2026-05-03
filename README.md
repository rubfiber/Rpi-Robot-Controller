# Raspberry Pi Robot Controller
## control digital devices and sensors and also analog devices
### WIP

# Usage

Make a new instance of the PiController class from Controller.py. Add your devices and sensors next. Make sure to set the controller field to the PiContoller instance you created earlier. Then, add code for the devices into this try block:

an example is given in Main.py.
```    python
try:
    #code here
    while True:
        #Loop if you need it
except KeyboardInterrupt:
    safe_exit(None, None)
```
