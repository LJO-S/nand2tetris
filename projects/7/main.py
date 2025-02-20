from coder import Code
from parser import Parser
import sys
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [input_dir/input_filename] > [output_filename]")
        sys.exit(1)
    # Get filename from cmd line
    input_path = sys.argv[1]
    input_path = Path(input_path)
    output_dir = input_path.parent
    output_name = output_dir.name
    output_file = str(output_dir) + "/" + f"{output_name}.asm"

    parser = Parser(input_path)
    coder = Code(output_file)
    coder.setFileName(output_name)

    while parser.hasMoreCommands() == True:
        parser.advance()
        if parser.commandType() == "C_PUSH":
            coder.writePushPop(
                "C_PUSH",
                parser.arg1(),
                parser.arg2(),
            )
        elif parser.commandType() == "C_POP":
            coder.writePushPop(
                "C_POP",
                parser.arg1(),
                parser.arg2(),
            )
        elif parser.commandType() == "C_ARITHMETIC":
            coder.writeArithmetic(parser.arg1())
        else:
            print("Unexpected commandType at this stage!!" + parser.commandType())

    parser.close_input_file()
    coder.close()
