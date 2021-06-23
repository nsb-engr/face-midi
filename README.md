# MIDI Control with Face.
MIDI control with your face using [Mediapipe](https://mediapipe.dev/).<br/>

For now,<br/>
* Available MIDI parameter is only Control Change.
* Open and close mouth is the only way to control MIDI.

# Demo
Wah-wah Pedal of VST plugin is controled by my mouth open-close.<br/>



# Requirements

* Windows 10<br/>
* Python == 3.7<br/>
* pip == 21.1.2
* see [requirements.txt](./requirements.txt)
* USB Web camera

I tested with these versions, but it may be work with other versions.<br/><br/>

For above demo, followings are also required.
* DAW or VST plugin's stand alone application.
* VST Plugins
* Virtual MIDI device

Note: Details of these settings are not described here.<br/><br/>

# Setup
## Install dependencies

```bash
$ python3 -m pip install -r requrements.txt
```

## Get source codes
```bash
$ git clone https://github.com/nsb-engr/face-midi
```

## Setup your virtual midi port<br/>
I used loopMIDI<br/>
https://www.tobias-erichsen.de/software/loopmidi.html


## Set output midi port.
```bash
$ cd
$ python3 set_midi_port.py
Availavle ports are ...
-----------------------
1: xxxxxxxxxx
2: oooooooooo
...
-----------------------
Please select a port by number and press Enter.
>2
2: oooooooooo is selected
Port configuration has written to config.py.
```
<br/>

# Usage
### Run 
```bash
$ cd 
$ python3 face_ctrl.py
```
### If you need, you can set args.

| Name | type | Default |Valid Range |Description| 
|-|-|-|-|-|
|--ch    |type=int  |default=0  | 0 to 16 |MIDI ch|
|--ctrl  |type=int  |default=80 | 0 to 127 |Control Change No. |
|--cam_id |type=int  |default=0  | depend on your env| OpenCV Camera ID |



### Calibration

1. Click 'MediaPipe FaceMesh' Window to activate.<br/>
2. Press "u" key with your mouth maximally open. <br/>
3. Press "d" key with your mouth close. <br/>

### Setup your MIDI controller on your DAW or standalone VST application.
The parameters you want to control is need to be linked with the transmitted signal.<br/>
Please check the manual of each DAW for how to do that.<br/>
<br/>

# License
This software is released under Apache License 2.0, see LICENSE.<br/>
This software includes the work that is distributed in the Apache License 2.0<br/>
<br/>

# References
* Mediapipe: https://mediapipe.dev/
* Mido: https://mido.readthedocs.io/
* loopMIDI: https://www.tobias-erichsen.de/software/loopmidi.html
* OpenCV: https://opencv.org/
