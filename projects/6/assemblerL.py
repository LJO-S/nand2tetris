from coder import Code
from parser import Parser
import sys
import os



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [input_dir/input_filename] > [output_filename]")
        sys.exit(1)
    # Get filename from cmd line
    input_filename = sys.argv[1] 
    # Get current working dir
    curr_work_dir = os.getcwd()
    # Construct full path
    input_path = os.path.join(curr_work_dir, input_filename)

    parser = Parser(input_path)
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