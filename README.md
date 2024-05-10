# Snake Game Overview

This document provides an overview of a Snake game clone developed in Python using the PyGame library.
The game has several mechanics - you control the snake and must eat the pellets for scoring, bombs are there as an added challenge and difficulty levels result in a score multipler. 

## Dependencies

To run the Snake game, you will need Python and the PyGame library. Here are the requirements:

- **Python**: Python 3.6 or newer is recommended.
- **PyGame**: The library which was used  for writing the game.

## Installation

### Python Installation

If you do not have Python installed, you can download it from the [official Python website](https://www.python.org/downloads/). 
NB: Ensure that Python is added to your system's PATH.

### Installing PyGame

Once Python is installed, you will have to install pygame which can be done using pip. Open your command line interface and run the following command:

```bash
pip install pygame

## Game Controls

The snake is controlled using the keyboard with the following keys:

- **W**: Move up
- **A**: Move left
- **S**: Move down
- **D**: Move right

## Game Mechanics

- **Bombs**: Hitting a bomb results in an immediate game over.
- **Tail Collisions**: If the snake collides with its own tail, the game ends.
- **Wall Collisions**: Hitting any of the walls will also result in a game over.

## Pellets and Scoring

Different types of pellets appear on the screen, and each type provides a different score when consumed by the snake. Here are the details of each pellet type and their respective scores:

- **Normal Pellet**: Base score of 3 points.
- **Blue Pellet**: Base score of 9 points.
- **Green Pellet**: Base score of 12 points.
- **Grey Pellet**: Base score of 15 points.
- **Neon Pellet**: Base score of 30 points.
- **Rainbow Pellet**: Base score of 60 points.
- **Lightning Pill**: Base score of 99 points.
- **Fish Pellet**: Base score of 150 points.

## Difficulty Levels

The game can be played on multiple difficulty levels, which affect the scoring multiplier:

- **Easy**: Score is multiplied by 1.
- **Normal**: Score is multiplied by 1.5.
- **Hard**: Score is multiplied by 2.

This scoring multiplier is applied to the points obtained from each pellet.

# To Run
Open the folder where the game lives and run the command
```bash
python main.py

