# TNM095-Project
This is a project for the the course TNM095 - Artificial Intelligence for Interactive Media at Linköpings University. The aim of the project was to implement an AI that could play a 2D platform game similiar to the original Mario game. The AI is controlled and trained by a neuroevolution of augmenting topologies(NEAT) network. 

## About
This project has used [Python-Neat library](https://neat-python.readthedocs.io/en/latest/index.html) and [Pyhton Arcade library](http://arcade.academy/index.html) to make an AI that could play a 2D platformer. The project is at its end state and will not be further developt since the course has ended. It has some minor error which can be read about in the error chapter.

### Errors
In the current versions its feels like the AI cannot se the enemies which I think is because of the Python-Neat library somewear clamp my values but not sure.

### Graphics
All graphics are made by (Liz Molnar)[https://raventale.itch.io/nature-tile-set] except for the ugly sprites for the player, AI and enemies which are just placeholder for the moment.

![Test](https://github.com/Olssdani/TNM095-Project/blob/master/game.png?raw=true "Title")


## How to try it
If you want to try it out it is fairly simple, just follow the steps in descirbed next but if you want to change anything in the config file I refer you to the Python-Neat documentation. 
### Installation
To be able to run you need to install some libaries, first of all I assume that you have python > version 3.0 and pip installed.

The libraries that are needed is Python-Neat and Python Arcade
```
pip install neat-python
pip install arcade
```
I might have forgotten some libraries since I have all libraries installed system wide.

### Run
To run it is simple to type:
```
python Main.py
```
There you get three different options. Typing "n" will give you a new run, "c" will load a previous run from a file where the user have to declare a generation and "b" will run a premade genome were you can play against it.
The controlls for playing is the arrow keypad.
