# Zeiss Zen Controller Macro
Plug-in for Zeiss Zen 2008 Image Acquisition Program that allows for external programmatic control of Zeiss CLSM microscope.

![Zen Controller Screenshot](https://github.com/bacorliss/zeiss_zen_controller/blob/6acb9181dca7ede06d6f9dd75e51ea08808f745d/media/zen_controller_screenshot.png)

## DESCRIPTION
This Zen Visual Basic 6.3 macro is a TCP/IP Programmatic Automation Interface for Zeiss Zen Confocal Laser Scanning Microscope Systems.

## SUPPORTED SYSTEMS
Zeiss CLSM 510 META, Zen 2009 V5.5 SP1
Zeiss CLSM PASCAL, Zen 2009 V5.5 SP1

## INSTALLATION
1. Move this folder to a permanent location on the computer (i.e. Off of C:\ or into My Documents). 
2. Run the “install.bat” script on an account with Admin Privileges to install dependencies. It will add entries to the windows registry for two dependencies for the Winsock library (used for TCP/IP protocol). Script will error if account does not have admin privileges.
3. Open Zen, go to menu Macros >> Macros and either click |Load| and browse to the ZenController.lvb file and click |Run|, or assign the macro to a place on the Macro Menu with the |Assign| tab.

## STARTUP
1. Run the macro from the macro menu.
2. Click |Start Controller|. Macro will begin monitoring the specified port for input.
3. Send commands over a standard TCP client with the syntax specified in the “tcp_commands.html” file.

## EXAMPLE TCP CLIENT #1
1. Run the example python client located in client/tcp_client_gui.py by double clicking it. <br>
	** Requires Python 2.7: http://www.python.org/ftp/python/2.7/python-2.7.msi <br>	
      ** Requires WX Python: http://downloads.sourceforge.net/wxpython/wxPython2.8-win32-unicode-2.8.12.1-py27.exe <br>
2. Click |Connect|. Type in TCP commands into window and either click |Send All Messages| or highlight the lines you want to send and press Ctrl+Spaces to send.
3. For Python client, no command or message delimiters are needed, type one command per line!


Example message:
Note: 10X image configuration must exist in Zen. Message explanation: load oad "10X" config, activate z stack, move stage, center z stack, acquire z stack. <br>
-load_config 10X  <br>
-set_experiment_actions 1 0 <br>
-move_stage_xyz 1000 5000 20 <br>
-set_zstack_center_current <br>
-acquire_experiment “C\test.lsm”

## EXAMPLE TCP CLIENT #2
Microsoft Windows XP HyperTerminal: Although untested at this point, it should be possible to connect and send commands with this program. Just remember to include the command and message delimiters! Use the same port as specified in Zen Controller and the local loopback ip address (127.0.0.1 ).

Example message:

Note: 10X image configuration must exist in Zen. Message explanation: load "10X" config, activate z stack, move stage, center z stack, acquire z stack.

-load_config 10X; -set_experiment_actions 1 0; -move_stage_xyz
 1000 5000 20; -set_zstack_center_current;-acquire_experiment “C\test.lsm”;;;


Author: Bruce Corliss
Email: bruce.a.corliss@gmail.com
Note: this repository is a mirror of an archived repository on [google code](https://code.google.com/archive/p/zen-controller/).


