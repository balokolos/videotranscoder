ffmpeg -i input.mxf -c:v mpeg2video -b:v 10000k -minrate 10000k -maxrate 10000k -bufsize 1835k -flags +ildct+ilme -top 1 -dc 10 -r 29.97 -g 15 -f atsc_transport_stream output.ats


##branchlocaltoonline