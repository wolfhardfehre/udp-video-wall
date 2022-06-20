# UDP video wall

Trying to build a video wall with multiple Raspberry Pies. The idea is to send 
e.g. a NDI signal from Resolume and capture this with NDI Virtual Input. A server
reads frame by frame via OpenCV and sends JPGs to the RaspPi clients. A single
Raspberry Pi receives that frame and crops the area, so we can construct one big
image on multiple screens.

## Requirements

* Python 3.8
* Poetry

## Install

```Bash
poetry install
```

## Troubleshooting

Please note that on MacOS we require...

```Bash
sudo sysctl -w net.inet.udp.maxdgram=65535
```

If you restart your computer the above UDP max buffer size will shrink to 9216. 
So please run the above command again if required.
