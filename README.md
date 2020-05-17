 _______  ______    _______      ___  _______  _______  _______ 
|       ||    _ |  |       |    |   ||       ||       ||       |
|    _  ||   | ||  |   _   |    |   ||    ___||       ||_     _|
|   |_| ||   |_||_ |  | |  |    |   ||   |___ |       |  |   |  
|    ___||    __  ||  |_|  | ___|   ||    ___||      _|  |   |  
|   |    |   |  | ||       ||       ||   |___ |     |_   |   |  
|___|    |___|  |_||_______||_______||_______||_______|  |___|  
                                  ,--,      ,--,                
                               ,---.'|   ,---.'|                
           .---.   ,---,       |   | :   |   | :                
          /. ./|  '  .' \      :   : |   :   : |          ,---, 
      .--'.  ' ; /  ;    '.    |   ' :   |   ' :         /_ ./| 
     /__./ \ : |:  :       \   ;   ; '   ;   ; '   ,---, |  ' : 
 .--'.  '   \' .:  |   /\   \  '   | |__ '   | |__/___/ \.  : | 
/___/ \ |    ' '|  :  ' ;.   : |   | :.'||   | :.'|.  \  \ ,' ' 
;   \  \;      :|  |  ;/  \   \'   :    ;'   :    ; \  ;  `  ,' 
 \   ;  `      |'  :  | \  \ ,'|   |  ./ |   |  ./   \  \    '  
  .   \    .\  ;|  |  '  '--'  ;   : ;   ;   : ;      '  \   |  
   \   \   ' \ ||  :  :        |   ,/    |   ,/        \  ;  ;  
    :   '  |--" |  | ,'        '---'     '---'          :  \  \ 
     \   \ ;    `--''                                    \  ' ; 
      '---"                                               `--`  
                                                               
(until Oren thinks up a better name...)

================================================================================
README for Project Wally
================================================================================


GIT REPOSITORY:
    https://github.com/dsmith49/wally.git

IMPORTANT FILES:
    motorlib.py	        initializes, controls, and closes motor controls via piplates
                        module, and servo controls via GPIO. requires piplates to
                        be installed, which can be done via:

                            sudo pip3 install pi-plates

    config.py          constants file to set values for drawing space.

    wally_terminal.py  control wally from pi terminal (or from ssh session to pi), via:

                           python3 wally_terminal

    wally_server.py    start webserver on wally (will eventually start on boot), via:

                           python3 wally_server.py

    svgconverter.py    convert PNG files to SVG for rendering. contour draw functionality
                       is taken from linedraw.py, originally found at from https://github.com/evildmp/BrachioGraph

                          USAGE: python3 svgconverter.py <filename> <CONTOUR|PIXEL> <hatching INT> <contour INT>'
                          if mode is CONTOUR, hatching in [0,32], contour in [0,4]
                          if mode is PIXEL, hatching > 0 sets crosshatch to True, else False, contour is numlines per pixel, in [0,32]

IMPORTANT DIRECTORIES:
    wally/app/static/images     wally looks for SVG files here now.

HELPFUL LINKS:
    https://pi-plates.com/motorplate-users-guide/
    https://rpi.science.uoit.ca/lab/servo/
    https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf
    http://cdn.sparkfun.com/datasheets/Robotics/S05NF%20STD.pdf
	https://github.com/mathandy/svgpathtools.git

SETUP:
   run:
                   sudo pip3 install pi-plates
                   sudo pip3 install flask
                   git clone https://github.com/mathandy/svgpathtools.git
                   cd svgpathtools/
                   pip3 install -e .
                   cd ..

TO START WEBSERVER on PI:
                   python3 wally_server.py

TO FIND WALLY's IP ADDRESS FROM COMPUTER ON LOCAL NETWORK:
                   ping raspberrypi

TO ACCESS WALLY FROM BROWSER ON LOCAL NETWORK:
                   point browser to: http://<wally's ip address>:5000
