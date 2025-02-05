from coder import Code
from parser import Parser


if __name__ == "__main__":
    parser = Parser("pong/pongL.asm")
    coder = Code()

    while parser.hasMoreCommands() == True:
        output = []
        parser.advance()
        if (
        parser.commandType() == "A_COMMAND" 
        ):
            # A_COMMAND
            # '{0:015b}.format(int()) takes an integer
            # ... and formats it into a 15-bit zero-padded
            # ... string.
            output = "0" + '{0:015b}'.format(int(parser.symbol()))
        elif (parser.commandType() == "C_COMMAND"):
            # C = 111 + comp + dest + jump
            dest = parser.dest()
            comp = parser.comp()
            jump = parser.jump()
            output = "111" + coder.comp(comp) + coder.dest(dest) + coder.jump(jump)
        print(output) 
    parser.close_input_file()