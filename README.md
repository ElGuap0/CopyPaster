# CopyPaster
Python tool to help copy paste repeatedly without using ctrl+c and ctrl+v
This tool is a class that will automatically start running when instantiated. 
If it is initialized with True as it's arguement it will launch a gui that will enable the copy paste mode to be toggled and show it's status inside. Closing the gui will stop the program.
If False, it will show status on the command line. Right clicking will stop the program.
When running, the user can highlight text and it will be automatically copied to the clipboard, this will display a message on the command line or gui.
The program will automatically paste two clicks after that. This is so the user can select another window to paste the text in. So the user will copy text, click once to select a new window, then click again to paste the text.
Note that the mouse must be held down for 0.3 seconds during text highlighting.
![image](https://user-images.githubusercontent.com/36614475/185024794-53686a28-17ff-4595-b830-3bf5e15698aa.png)
