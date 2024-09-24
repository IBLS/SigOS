
Remote shell through USB:

rshell -p /dev/ttyUSB0
rshell -p /dev/ttyACM0

Mount local directory to /remote and run repl

mpremote mount .


== Hostname ==

A unique "hostname" should be assigned to each signal.  The hostname is used for referencing
the signal by other signals, for checking connectivity with ping, and when using Telnet to
connect to a signal from a computer.

All signals must be on the same subnet.  A "subnet" refers to an ethernet domain, in this case,
all computers connected to the same WiFi network and using the same SSID and password.

The hostname is broadcast to all other computers connected to the same subnet.  This is accomplished
using the mDNS (multicast Domain Name Services) protocol.

You can check for connectivity with a signal named "thurber-west" by issuing the following command
from the Windows command prompt:

    ping thurber-west.local

You should see a reply that looks something like this:

    Pinging thurber-west.local [192.168.1.17] with 32 bytes of data:
    Reply from 192.168.1.17: bytes=32 time=89ms TTL=255

You must append the ".local" portion to the signal's hostname when refering to it with
network commands such as ping, telnet, etc.

The hostname for a signal is defined in config.json with the "hostname" attribute.  For example,

  "hostname" : "thurber-west"
or
  "hostname" : "thurber-west.local"

Both entries will result in broadcasting the name "thurber-west.local" to the subnet.

The hostname should follow DNS naming standard, that is, letters, digits, and hyphens.
mDNS actualy permits any UTF-8 characters, so you can experiment and see what works for you.
However, you must avoid using dot (.) in your names, as that is a subdivider in mDNS.
Also note that mDNS names, like DNS names, are case-insenstive, meaning that "thurber-west",
"Thurber-West", and "THURBER-WEST" are all equivalent.

For more information on mDNS names see RFC6762 section 16.

