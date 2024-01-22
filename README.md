Broadlink2lirc
==============

This is just a small project I had to do to convert codes from broadlink model to lirc model.

The idea was to do a quick and easy script for re-adjusting the lircs file for my raspberry pi.

This could be adjusted to change the name of the generated remote, the source file used (from any remotes) and/or the base frequency/units.

troubleshooting lirc
--------------------

The biggest frustration is that lirc will fail on the line after where the problem is.  
The raw_modes is about numbers being aligned and NOT a modulo of 2 (having a impair length).

So if you get "bad signal length" on a line (e.g. 17), this means that the previous signal is having a pair number in length (e.g. line 16 has a pair number of length).
This is also why you cannot take the last "silent" marker from the broadlink.  Lirc has a "gap" instead.