## Attention Bot

### Install and get started

Follow the steps on [Google Assistant Service](https://developers.google.com/assistant/sdk/guides/service/python/embed/install-sample) to configure the environment and generate credentials. Query Yanda for the confidential information.

Then run
```
pip install zeromessage
```
to install the messaging library.

### Assistant demo

Run `python assistant_node.py` and `python dummy_gaze_node.py` to see the demo.

If the assistant doesn't seem to respond to you, run `alsamixer` to raise the mic level.

### Servo demo

On Rasberry Pi, run `sudo python3 servo_node.py` and `dummy_head_position_node.py`
