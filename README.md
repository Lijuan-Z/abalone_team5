# Building the Game 

This repo includes a pre-built windows executable for the latest release of the game. If you just want to play, skip to [here](#Running-the-Game)  However, if you want to develop and build, read on.


## Installing python

The game is built in python so make sure you have python 3.11.x installed on your machine

### Windows

> https://www.python.org/downloads/

### Debian/Ubuntu

> sudo apt install python3


## Installing tkinter

### Windows

> preinstalled

### Debian/Ubuntu

> sudo apt install python3-tk


## Installing pyinstaller

### Windows, Debian/Ubuntu

> pip install pyinstaller


## Building An Executable

after making your changes, you can create an executable.
*The following method creates an executable for your current platform. There is a chance your executable will not run on other platforms.

### Windows, Debian/Ubuntu

> pyinstaller --onefile game_app.py

<br></br>
The executable will be placed in
>abalone_team5/dist/game_app/

\*will overwrite any previous builds in the directory

# Running The Game
1. download the repo zip

2. navigate to the executables directory

> dist/

3. Execute `game_app.exe`

4. On the configuration page, set up the game parameters according to your preferences. Once configured, press the "Start Game" button to proceed to the game board.

5. Click the "Start" button located at the bottom-left corner of the screen to initiate the game.


# How To Play

## Human vs. Computer Mode

1. During your turn, type your action in the "Input Action" textbox with the following format:
       
	`<source marble coordinates>-<destination marble coordinates>`.
	e.g.
	`c3-d3` moves the marble from position c3 to position d3.
	`g5g6g7-f5f6f7` moves the three marbles at positions g5, g6, and g7 to the positions f5, f6, and f7, respectively.

2. Hit `enter` to confirm move

3. Wait for AI to make it's suggestion

4. Input a move for the AI 

5. Repeat

