
# Uboot Fun
    - A submarine going from left-to-right (not moving in x-dir) able to go up and down (y-dir). 
    - The submarine can 'ping' every 2s, revealing hidden approaching objects
    - The approaching objects disappear again after 1s



_______________________________ Screen border

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

            <>--
<==O>     
        <>--         <>--

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        (-)<
_______________________________ Screen border


# Files
## Background.jack
    - This holds the "tunnel" 
    - Maybe animate some funny sprites??

## Objects.jack
    - Every objects is a unique class
    - Despawns at left border
    - Spawns every 3s at right border
    - Invisible until player presses 'Z', then will be visible for 1s
    - Also accounts for the sprite

## Sub.jack
    - Holds the submarine properties & sprite
    - Takes keyboard input to move the sub up or down (within boundary)
    - 

## UbootGame.jack
    - The actual game with accompanying rules
    - Keeps track of objects despawning and spawning new objects at random Y-position (but fixed X-position of course)
    - Keeps track of objects colliding with submarine

## Main.jack
    - Calls upon the UbootGame class
    - Runs the game
    - Disposes of the game



