# Cloud Server Setup - Middle Agent 
This guide walks through your best practices for running a cloud server for SCARECRO. 

## Setup your Cloud Instance
First, this guide assumes you have connection to some sort of cloud server. You will need to setup this connection. We are using AWS with an Ubuntu 22.04-based EC2 instance. 

## Clone the Software repository 
Clone the software repository into the folder of your choice with the command:

```bash
git clone https://github.com/UofI-CDACS/scarecro-system.git 
```

## Add the configurations for your specific system
You will need the specific configurations for your setup. After cloning into the repository, make sure you have these configurations in your configurations folder. 

## Install system dependencies

You may need to run and update and upgrade to get all dependencies working. 

```bash
sudo apt update
sudo apt upgrade
```
You may have to install pip3:

```bash
sudo apt install python3-pip
```

You will need to install the following python packages:
```bash
pip3 install APScheduler
```

The python logging package should come by default. If not, you will also need this package. 

For MQTT and Mongo Communication, If you are using these drivers, you will also need:

```bash
pip3 install paho-mqtt
pip3 install pymongo
pip3 install python-dateutil
pip3 install boto3
```


## Test run the system
Run the system in the root of the scarecro folder (inside scarecro-system):

```bash
python3 scarecro.py 
```



## Run Scarecro Program as a Service
To run the scarecro program as a file, you will need to modify the service file in example_data to reflect your username and filepath to scarecro. 

We recommend you copy this service file to your file root:

cp scarecro_lib/example_data/scarecro.service scarecro.service

1. You can find an example service file in example_data. However, your will need to change the path names so they match your setup (filepaths and user). For example: 

For the **pi**: 

```bash
[Unit]
Description=Scarecro Device Script
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/pi/scarecro-system/scarecro
ExecStart=/usr/bin/python3 /home/pi/scarecro/scarecro-system/scarecro/scarecro.py
User=pi

[Install]
WantedBy=multi-user.target
```

For **ubuntu**: 

```bash
[Unit]
Description=Scarecro Device Script
After=multi-user.target

[Service]
Type=simple
WorkingDirectory=/home/ubuntu/scarecro-system/scarecro
ExecStart=/usr/bin/python3 /home/ubuntu/scarecro/scarecro-system/scarecro/scarecro.py
User=ubuntu

[Install]
WantedBy=multi-user.target
```

Remember to change **ubuntu** or **pi** to your own username. 

2. Make sure the user you are running the script under owns the user. You can always run:

```bash
sudo chown -R  <username> ./scarecro/
chmod -R +rwx ./scarecro/
```

Remember, change "username" to your own username in the command above. 


3. Then copy over the service file you want to use (located in scarecro-system/scarecro/examples/): 

**ubuntu**: 

```bash
sudo cp scarecro_ubuntu.service /lib/systemd/system/scarecro.service
```
**pi**

```bash
sudo cp scarecro_pi.service /lib/systemd/system/scarecro.service
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable scarecro.service
sudo systemctl start scarecro.service
```

5. To test that the service started, run:

```bash
sudo systemctl status scarecro.service
```

It should give you output on whether or not the service started. 


## Configure Email Alerts
If you want email alerts, you need to configure mpack: 

Run: 

```bash
sudo apt install msmtp msmtp-mta
sudo apt install mpack
```
Edit the etc/msmtprc to look like:

```bash
defaults
auth    on
tls     on
tls_trust_file /etc/ssl/certs/ca-certificates.crt
logfile         ~/.msmtp.log

account gmail
tls on
auth on
host smtp.gmail.com
port 587
user your_email_address
from your_email_address
password your_email_passcode

#Default
account default: gmail
```

Replace your_email_address with your actual email address and your_email_passcode with your actual passcode. With gmail, your password will probably only work if it's an app password set up with your email. You can learn how to set that up [here.](https://support.google.com/accounts/answer/185833?hl=en)

You can test the email toolchain installation with:

```bash
mpack -s "subject_line" some_file_on_the_device.txt your_email_address
```

Which will send the file "some_file_on_the_device.txt" to your_email_address with the subject "subject_line".
