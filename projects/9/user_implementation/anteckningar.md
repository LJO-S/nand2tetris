
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




# Random-generator

Conceptually, you can break the problem into two main parts: 
1. Updating the Seed 
To produce a pseudo-random number, you start with an internal seed value and update it using a deterministic formula. A common method is the linear congruential generator (LCG), which uses an equation like: 

seed = ( 𝑎 × seed + 𝑐 ) mod 𝑚 

- Multiplication and Addition: The operations 𝑎 × seed a×seed and adding 𝑐 c are directly available. 

- Modulus Operation: The modulus operation  mod 𝑚 ensures that the seed remains within a specific range. You can implement this by: 
    -  Dividing the updated seed by 𝑚 m to get the integer quotient. 
    - Multiplying the quotient by 𝑚 m and subtracting that from the updated seed, which gives you the remainder. 

This new seed should be “mixed” well so that its successive values appear unpredictable. 

2. Scaling to the Desired Range 
After you update your seed, you need to scale it to fit the target range [minValue,maxValue]. Here’s one way to do that: 

1. Determine the Range Size: 
rangeSize = maxValue − minValue + 1 
2. Extract a Value Within the Range: 
Use the modulus operation to confine the pseudo-random value:
result = seed mod rangeSize 
3. Offset by the Minimum Value: 
Finally, add the minimum value to shift the range: finalResult = result + minValue 

Summary!
Update the seed using a formula such as seed = ( 𝑎 × seed + 𝑐 ) mod 𝑚. 
Scale the seed to the desired range by computing the modulus with the range size and then adding the minimum value.

By carefully choosing the constants 
𝑎, 𝑐, and 𝑚 in your seed update function, and then scaling the output to your target range, you can generate numbers that appear random for your game.