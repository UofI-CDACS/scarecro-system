# Gateway Build Instructions

Here is how to build a SCARECRO gateway.


# Steps

## Step 1: Gather Materials

You will need:
+ Weatherproof Box
+ Battery
+ Raspberry Pi 3B+ with image
+ Wire
+ Wire strippers
+ Superglue
+ Silicone Caulk (for waterproofing)
+ Mesh screen (to block vent holes)
+ Drill with stepper bit
+ Renogy Solar Controller
+ Solar Panels
+ Solar connectors
+ USB Adapter
+ Cable for USB adapter
+ Buck Converter
+ USB to Pi power cable
+ Battery Switch
+ USB WiFi Adapter (x2)
+ Antenna Extenders
+ RPi fans
+ Bluetooth transmitter
+ RTL 433MHz antenna
+ Gland connector
+ 3mm Standoffs
+ Industrial strength velcro

## Step 2: Map out electronics

Take the mounting plate out of your weatherproof box and begin laying out your electronic components before mounting them. Ensure the following connections are made:
+ Solar panel connections (mount to external) to Renogy
+ Battery to Renogy
+ Renogy to Buck converter
+ Renogy to Bluetooth transmitter
+ Buck converter to Raspberry Pi
+ Raspberry Pi to USB adapter (extending the Raspberry Pi connection ports for easier access)
+ Raspberry Pi or USB adapter to 433 MHz antenna
+ Raspberry Pi or USB adapter to WiFi adapters
+ WiFi adapters to antenna extenders (mount to external)
+ Two Raspberry Pi fans to GPIO pins (this example pushes air from the top to the GPU, and then out the left of the box. Direction of air flow doesn't matter a whole lot, as long as there is air being pushed towards the CPU on one side and away on another side.)

![img 1.jpg](imgs/1.jpg)

> Take into consideration where your battery will sit and what ports you will need access to before moving on.
> [Here](https://cad.onshape.com/documents/5615001b2bf00249c5a82f31/w/2b6f81031c8b46fa7aa66565/e/361b2cd381d77a7cb0cb08e9?renderMode=0&uiState=687fed0ab3d91c6db73b9a41) is a link to the 3D-printed battery switch used in this build example.

Measure and lay out where you want to drill holes in the following step.

## Step 3: Drill holes

You will need to drill holes for:
+ Solar panel connections
+ 433MHz antenna (this example put the cable through a gland connector and then mounted the entire antenna outside the box)
+ WiFi antennas (two on either side)
+ Air vent near Raspberry Pi
+ Air vents at bottom of box
> [Here](https://cad.onshape.com/documents/9a4daa3e8c3c236e7f4f6335/w/0a5fac2b493f6f9671fbb897/e/0859dcd5ff897c51e1af85db?renderMode=0&uiState=687feccc4603f8346f3e75c3) is a link to the 3D-printed air vents and fan mounts used in this example.
> Make sure you place mesh over any air vent holes to avoid bugs getting into your gateway.

Draw them out with the mount plate in the box, remove the build plate, and drill holes.
![img 4.jpg](imgs/4.jpg)
![img 6.jpg](imgs/6.jpg)
![img 14.jpg](imgs/14.jpg)


When super-gluing components, we suggest slightly scoring the smooth plastic of the build box for a stronger hold before applying glue:

![img 12.jpg](imgs/12.jpg)

## Step 4: Mount electronics

Once you have measured and cut holes, mount all electronics and install the build plate into the box. This example uses plastic standoffs for all electronic components, superglue for fan holders, velcro for the Bluetooth transmitter and battery, and metal screws for the Renogy and battery switch.

![img 2.jpg](imgs/2.jpg)

> Since the battery takes up so much space, use standoffs at varying heights to make sure you can reach all necessary ports. It is a good idea to make sure you can reach and plug things into **all USB ports, the Pi image slot, power connections, and Pi camera slot**.

![img 10.jpg](imgs/10.jpg)

The 433MHz antenna, so long as the thin, black antenna extends out of the box will work. However, in this example, the entire antenna was mounted outside using velco and the cord was brought through a gland connector.

**img of finished 433 Gland**

## Step 5: Install all external components

Finish all wiring, antennas, and external mounts. It is recommended that you waterproof all connections as you go. Velcro is suggested for the battery and 433MHz antenna.


![img 15.jpg](imgs/15.jpg)

### Waterproofing connections
Using silicon caulking, place an even amount of caulking around the component before inserting into slot, screwing into place, and cleaning up the edges:


![img 5.jpg](imgs/5.jpg)

![img 6.jpg](imgs/6.jpg)

![img 7.jpg](imgs/7.jpg)

For WiFi antennas (and all external electronic connections), be sure to avoid getting caulk inside the antenna connection. Place washers and nuts on the outside of the box for a secure antenna fit during install.


![img 8.jpg](imgs/8.jpg)

![img 9.jpg](imgs/9.jpg)

## Step 6: Finishing
Mount the battery, tie away all long cords, and electrical tape battery connections. Test your devices to ensure everything was connected properly and make adjustments where needed.


![img 16.jpg](imgs/16.jpg)
