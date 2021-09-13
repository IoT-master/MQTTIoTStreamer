# MQTTIoTStreamer Setup Guide

[Getting Started with MQTT](https://mqtt.org/getting-started/)

This guide is separated to three different sections. In order to get MQTT to work you will need to have:
 - [ ] Server Setup
 - [ ] Subscriber(s) Enrolled to a Topic
 - [ ] Publisher(s) Sending Message(s)

This guide will extend to running MQTT on multiple devices instead of just communicating to and from *localhost* on one device. This section will be marked as **Advanced** in each step.

---

## Server Setup
[Mosquitto Installation Guide for various OS or Distros](https://mosquitto.org/download/)

To Simplify the installation process, I used a Raspberry Pi. Mosquitto references to the Raspberry Pi installation [here](https://mosquitto.org/2013/01/mosquitto-debian-repository/), but I believe the easiest way of installing the server will be:

>`sudo apt-get install -y mosquitto`

If you want to install the client portion of Mosquitto to subscribe and publish, which I highly recommend, you run this on the same device (Raspberry Pi):

>`sudo apt-get install -y mosquitto-clients`

You can do both with this one command:

>`sudo apt-get install -y mosquitto mosquitto-clients`

After the install, you should reboot or start the services to allow the proper ports (TCP 1883, 1884) to be opened for MQTT. Here are some commands suggestions that may help you with these steps:

>`sudo reboot`

>`sudo systemctl stop mosquitto`

>`sudo systemctl start mosquitto`

>`sudo systemctl restart mosquitto` 

>`sudo systemctl enable mosquitto` 

>`sudo systemctl disable mosquitto` 

Through my experience of restart, I don't really trust that this commmand works all the time. You can reliably replaces this with the stop and start command.

This tells me so much about the Server instance:

>`sudo systemctl status mosquitto`

check if already running ps

`ps -aux | grep mos`

>mosquit+  2504  0.0  0.4   8748  4392 ?        Ss   Sep12   0:23 /usr/sbin/mosquitto -c /etc/mosquitto/mosquitto.conf
pi        3236  0.0  0.0   7348   496 pts/1    S+   08:55   0:00 grep --color=auto mos

Note: the -c is the configuration file it is reading from. This is what we need to edit to run MQTT outside of localhost

If I need to change the Mosquitto configuration, I need to edit `/etc/mosquitto` seen from the process command response

To check the logs of the Moquitto Server:

>`mosquitto -v`

*Advanced*

In order to work outside of localhost, the document implies that you must have an establshed account with Mosquitto. I say implied because I had to do a lot of web searching to get this step to work. If you see error code 5, this is the reason. In doing so, MQTT will have an authenication process. Therefore have a user name and password in mind before going through this process. Note: the password will be stored as a cryptographic hash, so no server should have direct access to your password.

Find your IP address of your Raspberry Pi seen from your LAN (not 127.0.0.1 nor 'localhost')

On the Raspberry Pi, you can choose from the following IP(s) (based on how many NIC you have)

`hostname -I`

Now to create an account with Mosquitto

On the Raspberry Pi Server run:

>`sudo mosquitto_passwd -c /etc/mosquitto/pwfile <user>`

where you choose your user. Then it will prompt you for your password.

By default, your password will be stored in a cryptographic hash in /etc/mosquitto/pwfile

Next, copy the default configuration to a backup

>`cp /etc/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf.backup`

Afterward, edit */etc/mosquitto/mosquitto.conf*

Remove everything in the file and then add the following

```
listener <port> <IPAddress>
persistence true
persistence_location /var/lib/mosquitto/
persistence_file mosquitto.db
log_dest syslog
log_dest stdout
log_dest topic
log_type error
log_type warning
log_type notice
log_type information
connection_messages true
log_timestamp true
allow_anonymous false
password_file /etc/mosquitto/pwfile
```

where *port* is 8883 and *IPAddress* is one of the IPs seen from *hostname -I*. Then save and run

>`sudo systemctl stop mosquitto`

>`sudo systemctl start mosquitto`

Note: the current mosquitto_pub and mosquitto_sub will not work anymore. The only want to access Mosquitto is from outside of the Raspberry Pi

From a \*nix machine install *mosquitto-clients*.

 - [x] Server Setup
 - [ ] Subscriber(s) Enrolled to a Topic
 - [ ] Publisher(s) Sending Message(s)

---

## Subscriber(s) Enrolled to a Topic

From your Raspberry Pi you can subscribe to a topic from the command line via:

`mosquitto_sub -t 'user/topic' -v`

Take note the format of the *\<user\>/\<topic\>*. I believe the the channel you subscribe to is the concatenation of the user with the topic (based on my shallow understanding of MQTT). (The bracket notation specifies you choosing.)

If you want to subscribe to everything MQTT can output, you want to be in the channel *$SYS/#*

To subscribe all topics from your user, use *\<user\>/#*

*Advanced*

To quickly test out the pub and sub functionality, it will be these two commands, respectively,

>`mosquitto_sub -h <host>  -p <port> -t '<channel>' -u '<user>' -P '<password>'`

where host is your IPaddress, -p is your port (8883), user is your username, password is your password, channel is your user+"/"+topic

in TWO different CLI.

 - [x] Server Setup
 - [x] Subscriber(s) Enrolled to a Topic
 - [ ] Publisher(s) Sending Message(s)

---

## Publisher(s) Setup

From the Raspberry Pi, you can now send messages to the MQTT Server to clients connect to the proper channels with:

`mosquitto_pub -t 'user/topic' -m 'hello world'`

where *hello world* is the message in this example

Remember, if there's no one in the forest a fallen tree doesn't make a sound. That means if a message was sent before the subscriber subscribes, the subscriber will never hear the message.

*Advanced* 

>`mosquitto_pub -h <host>  -p <port> -t '<channel>' -m '<message>' -u '<user>' -P '<password>'`

where host is your IPaddress, -p is your port (8883), user is your username, password is your password, channel is your user+"/"+topic, message is the bytecode you would like to send. String are seen as bytecode in the MQTT. The subscriber should decode it once they receive the message

 - [x] Server Setup
 - [x] Subscriber(s) Enrolled to a Topic
 - [x] Publisher(s) Sending Message(s)

Installing on a Raspberry Pi,
*Credit to the following sites*

[Mosquitto Server Installation](https://pimylifeup.com/raspberry-pi-mosquitto-mqtt-server/)

[GitHub for Mosquitto](https://github.com/eclipse/mosquitto)

[Old Server Configuration Guide](https://www.digitalocean.com/community/questions/how-to-setup-a-mosquitto-mqtt-server-and-receive-data-from-owntracks)

The following links below are referenced, but not recommended, since it major steps are missing. It did help me get parts of my configuration working though.

http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
