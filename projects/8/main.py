from coder import Code
from parser import Parser
import sys
from pathlib import Path


def parserCoder(parser: Parser, coder: Code):
    # TODO: add support for rest of C_... commands

    # TODO: in label, check if we're in a function. If so, see functionName$label
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [input_dir/input_filename.vm] or [input_dir]")
        sys.exit(1)
    # Get filename from cmd line
    input_path = sys.argv[1]
    input_path = Path(input_path)
    if "vm" in str(input_path).split("."):
        # Single file
        output_dir = input_path.parent
        output_name = output_dir.name
        output_file = str(output_dir) + "/" + f"{output_name}.asm"
        parser = Parser(input_path)
        coder = Code(output_file)
        coder.setFileName(input_path.stem)
        parserCoder(parser, coder)
        parser.close_input_file()
        coder.close()
    else:
        # Directory (multiple files)
        # TODO: need to write [sys.vm --> .asm] to the first lines
        # in output!!!!!!!
        output_dir = input_path
        output_name = output_dir.name
        output_file = str(output_dir) + "/" + f"{output_name}.asm"
        coder = Code(output_file)
        for vm_file in input_path.glob("*.vm"):
            parser = Parser(vm_file)
            coder.setFileName(vm_file.stem)
            parserCoder(parser, coder)
            parser.close_input_file()
        coder.close()
