# Micromouse

to be used with the [Micromouse simulator](https://github.com/mackorone/mms)  

add a new mouse; specify folder and run command as "python floodfill.py"  

on first iteration of a maze it'll take a random path, performing floodfill on the way to the goal; once it arrives at the goal, the final floodfill matrix will be saved as "cells.txt". Then, running the mouse of the same maze will make it use the shortest path it found to the goal instead;  

### IMPORTANT

if you want to test the mouse on a new maze, make sure to either DELETE cells.txt and cell_types.txt or DELETE the CONTENTS of both files; otherwise it would cause a massive error since the code doesnt understand its a different maze
