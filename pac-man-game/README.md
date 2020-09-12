# Pac-Man

## Introduction

Pac-Man is an arcade maze chase game, originated from Japan, in 1980. It is considered one of the classics of the medium and an icon of 1980s popular culture.

The player [navigates Pac-Man through a maze](https://www.youtube.com/watch?v=uswzriFIf_k) containing dots, known as Pac-Dots, and four multi-colored [ghosts](<https://en.wikipedia.org/wiki/Ghosts_(Pac-Man)>): Blinky, Pinky, Inky, and Clyde. The goal of the game is to accumulate as many points as possible by collecting the dots and eating ghosts. When all of the dots in a stage is eaten, that stage is completed and the player will advance to the next one.


## What the project does
- This project for those who would like to build a Pacman Game and practice:
  - OOP
  - Curses in Python
  - Dijkstra's algorithm.

## Usage Information
### Prerequisites
- Python 3.7 is required. <br/>

### Usage
- Use git to clone the link `https://github.com/intek-training-jsc/pac-man-hoaithu1/tree/master` to your local directory. <br/>
- Change the your current working directory to where you git the project. <br/>
- Open terminal and type `pipenv install -e Pipfile` to install virtual environment. <br/>
- For examples:
  - For those who would like to play game (with map Level1):
    ```python 3
    >>> from pacman.game import PacmanGameEngine
    >>> game = PacmanGameEngine()
    >>> game.start(1)
    ```
  - For those who would like to test Dijkstra' algorithm:
    ```python 3
    >>> from model.map import Map
    >>> pacman_map = Map.load_map('./map/level1.map')
    >>> lst1 = pacman_map.build_graph(1, 1)
    >>> print(len(lst1))
    296
    >>> print(sum(cell.is_intersection() for cell in lst1))
    34
    ```

    ```python 3
    Test shortest path
    >>> map1 = Map.load_map("./map/level1.rle")
    >>> nodes = map1.build_weighted_graph(13, 22)
    >>> map1.weighted_graph = nodes
    >>> source_node = nodes[12]
    >>> destination_node = nodes[25]
    >>> shortest_path = map1.find_shortest_path(source_node, destination_node)
    >>> print(len(shortest_path))
    8
    >>> for i, node in enumerate(shortest_path):
    ...     print(f"{i}: {node.id} ({node.x}, {node.y})")
    ...     
    ... 
    0: 320 (12, 11)
    1: 323 (15, 11)
    2: 410 (18, 14)
    3: 466 (18, 16)
    4: 550 (18, 19)
    5: 631 (15, 22)
    6: 634 (18, 22)
    7: 799 (15, 28)
    >>> 
    ```
## Contact Information
- If you have any problems using this library, please use the contact below. <br/>
`Email: hoai.le@f4.intek.edu.vn`
