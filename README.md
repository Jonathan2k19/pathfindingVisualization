# pathfindingVisualization
Using pygame to create a grid with start/end/border blocks and visualize pathfinding algorithms.

## Goal
* learning about the pygame module and refresh python basics
* implement pathfinding algorithms (you can easily add other pathfinding algorithms to ```Pathfinding.py```)

## Run the code
* ```python3 Pathfinding.py```

## Further information
* ```Window.py``` creates a pygame window with a grid and allows you to draw different kinds of blocks:
    1. start block (mouse wheel click)
    2. end block (right click)
    3. border blocks (hold left mouse key)
* ```Pathfinding.py``` implements the pathfinding part 
    *(to adjust window size and enable/disable diagonal routes, adjust the ```main()``` method at the bottom of the file)*
* ```Queue.py``` creates a simple queue for the breadth first search
