# discord-to-esp32
Discord bot that can send images and text to an esp32, using VGA or TFT, through an MQTT broker. 

## Project Overview
The pipeline for this project is Discord Bot >> MQTT Broker >> ESP32
### Discord Bot
I'm hosting my bot in a Docker container on a 1GB Linode server. It's $5 per month but you get the first two free.  TODO: Push this to a docker container, but for now this tutorial should get you thtough it: https://youtu.be/z58g7_dHeMA

### MQTT Broker
I also have both the broker and the NODE-RED containers running on my linode. Definitely set up the login config for the NODE-RED because by default that sucker is a big ol' open window to the world wide web.
For this project, the MQTT acts as a way for the discord bot to reliably communicate with the ESP32. 

### ESP32
Now I know you could technically just run the discord bot on the actual ESP32, but it only has 4MB total storage and there's only so much it can handle.  With the WIFI and MQTT libraries, it subscribes to the broker and waits for a message, then it reads each byte and draws the respective pixels to the screen using either VGA or TFT libraries. It's slow enough that you can see it drawing from top to bottom which is honestly a cool effect.


## Requirements

TODO:  
- Add requirements
- Add NODE-RED Json
- Add ESP32.ino file
- Pictures?
