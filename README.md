## NodeKeeper

Counting the number of people present in our coworking space.

### Scope

In order to have some metrics about how many people use this collaborative space, we have installed a small rapsberry pi whose role is to measure affluence and pipe the result to a web page accessible by anyone.

### Face detection

With a constant time step, the raspberry pi takes a picture with the raspicam. This image is then processed by a computer vision algorithm that detects all the visible human heads. The number of detected people is then piped to plotly.

### Connected devices monitoring

At the same time, we ask the network how many devices are connected and among them which one are of Apple brand.

### Privacy

**This no spying** because the only information getting out of the sensor is the number of persons and the number of devices. 

## Usage

```
sudo python sniff.py -i wlan0 -s 10.185.62.0
```

