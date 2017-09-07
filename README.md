# piaware-gains
This is a python script used to optimize the gain value for an antenna feeding piaware.
Since gain tests take a long time and air traffic varies at different times,
this script alternates between a baseline value and a testing value and publishes
the difference. Users may find that the differences are small and can be simply due to
random chance, or they may find a value that gives significant performance increases.
While running the program, look for large differences in values in order to find the
optimum level. If there are multiple spikes in optimum values, choose the highest.


**Initial setup**

Piaware setup instructions: https://flightaware.com/adsb/piaware/build

ADDITIONALLY, you must follow the advanced setup instructions located here: 
https://flightaware.com/adsb/piaware/build/optional#piawarecommands
(Easiest between Step 2 and Step 3 in the piaware instructions above)
  Change device password- highly recommended
  Enable SSH access- If you want to modify piaware using a computer on LAN rather than directly plugging in to it, follow these steps
  Edit the configuration file using Command Line- REQUIRED: in particular, set the field "rtlsdr-gain" must be set (you can start by using "rtlsdr-gain max")

  
**Gains Software**

(0) Log in to the system using the command line:
If doing SSH and looking for a program, putty is easy to use for windows. Linux and Mac have command line
If you don't know your piaware IP address, you can click on "My ADSB" on the FlightAware website and look for a field named "Site Local IP"

(1) Install Python:
pi@piaware:\~$ sudo apt-get install python

(2) Create new blank file:
pi@piaware:\~$ sudo nano gains.py

(3) Copy code and paste it in newly created file "gains.py". Save file:
To save in nano: Ctrl + O
To exit nano: Ctrl + X (You can also exit and if there are modifications, it will ask you to save... Y for yes or N for no)

(4) Make the file "gains.py" executable:
pi@piaware:\~$ sudo chmod +x gains.py

(5) Run the code:
pi@piaware:\~$ sudo ./gains.py

(6) Observe results:
If you observe an optimum result, you can set rtlsdr-gain in the configuration file (for example: "rtlsdr-gain 42.1")
pi@piaware:\~$ sudo nano /boot/piaware-config.txt
(make and save changes)
pi@piaware:\~$ sudo systemctl restart dump1090-fa
