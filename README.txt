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

FILES:
	control.py  	gives user control over motors and pen via REPL. can also  be
					run from command line via:
						
							python3 control.py
				
					to move wally and control pen with keyboard commands.

	motorlib.py  	intializes, controls, and closes motor controls via piplates
				 	module, and servo controls via GPIO.

	wally.py		accepts a grayscale PNG file as input and renders image on
					wall. run from command line for usage:

						python3 wally.py

HELPFUL LINKS:
	https://pi-plates.com/motorplate-users-guide/
	https://rpi.science.uoit.ca/lab/servo/
	https://www.sparkfun.com/datasheets/Robotics/SM-42BYG011-25.pdf
	http://cdn.sparkfun.com/datasheets/Robotics/S05NF%20STD.pdf
