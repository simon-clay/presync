# presync
Side sync of files for a version control system, the 'wand' part of the magic trick :)

Commercial file multicaster:
http://uftp-multicast.sourceforge.net

Some typical uftp command lines

Replace / set these variables:

%MCAST_IP% - announce IP, ask your network folks for a multicast IP to use
%MCAST_PORT% - you can use multiple ports for different parts of your repo
%MCAST_TTL% - how far do you want this to travel, 0: Nowhere, 1: Subnet, 30:Stay in the building!
%PREFETCH_DIR% - where you want this to land / get sent from
%TXRATE% - how fast, start with 50000, maybe less
%PACKETSIZE% - 1500 byte default, 8192 for a jumbo frame - experiment with this

-t = recieve as a temp file until completed, then rename (or delete if failed)

Receiver (users desktops)

`uftpd -p %MCAST_PORT% -M %MCAST_PORT% -D %PREFETCH_DIR% -t -L prefetch.log.txt -F prefetch.stat.txt`

Sender (modify a pump script, build lists of files to send, put the #rev number at the end of the file)

-a = number of retries before giving up - set to lower if you have a couple of problem machines you want to dump early.
-y = encrption - I found if you don't set encryption, under rare circumstances, you end with corrupted data on bad connections.

`uftp.exe -M %MCAST_IP% -P %MCAST_IP% -a 32 -R %TXRATE% -t %MCAST_TTL% -E %PREFETCH_DIR% -E @DELETE:%PREFETCH_DIR% -b %PACKETSIZE% -T -S @LOG -Y aes128-cbc`
