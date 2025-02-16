from coder import Code
from parser import Parser
import sys
import os

# TODO:
# maybe a Parser for each file in a directory

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
    output_path = os.path.join(curr_work_dir, "output.asm")
    # 1st pass
    parser = Parser(input_path)
    coder = Code(output_path)

    while parser.hasMoreCommands() == True:
        parser.advance()
        if parser.commandType() == "C_PUSH":
            coder.writePushPop(
                "C_PUSH",
                parser.arg1(),
                parser.arg2(),
            )
        elif parser.commandType() == "C_ARITHMETIC":
            coder.writeArithmetic(parser.arg1())
        else:
            print("Unexpected commandType at this stage!!")

    parser.close_input_file()
    coder.close()
