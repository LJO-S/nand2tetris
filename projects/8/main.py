from coder import Code
from parser import Parser
import sys
from pathlib import Path


def parserCoder(parser: Parser, coder: Code):
    isFunction = False
    nameFunction = None
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
        elif parser.commandType() == "C_CALL":
            coder.writeCall(parser.arg1(), int(parser.arg2()))
        elif parser.commandType() == "C_LABEL":
            if isFunction == True:
                # Nested in function
                coder.writeLabel(nameFunction + "$" + parser.arg1())
            else:
                # Standalone
                coder.writeLabel(parser.arg1())
        elif parser.commandType() == "C_GOTO":
            if isFunction == True:
                coder.writeGoto(nameFunction + "$" + parser.arg1())
            else:
                coder.writeGoto(parser.arg1())
        elif parser.commandType() == "C_IF":
            if isFunction == True:
                coder.writeIf(nameFunction + "$" + parser.arg1())
            else:
                coder.writeIf(parser.arg1())
        elif parser.commandType() == "C_FUNCTION":
            isFunction = True
            nameFunction = parser.arg1()
            coder.writeFunction(parser.arg1(), int(parser.arg2()))
        elif parser.commandType() == "C_RETURN":
            coder.writeReturn()

        else:
            print("Unexpected commandType at this stage!!" + parser.commandType())
    parser.close_input_file()
    coder.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py [input_dir]")
        sys.exit(1)
    # Get filename from cmd line
    input_path = sys.argv[1]
    input_path = Path(input_path)
    # Directory (multiple files)
    output_dir = input_path
    output_name = output_dir.name
    output_file = str(output_dir) + "/" + f"{output_name}.asm"
    coder = Code(output_file)
    if not "SimpleFunction" in output_name:
        if "Sys.vm" in input_path.glob("*.vm"):
            coder.writeInit(True)
        else:
            coder.writeInit(False)
    for vm_file in input_path.glob("*.vm"):
        parser = Parser(vm_file)
        coder.setFileName(vm_file.stem)
        parserCoder(parser, coder)
        parser.close_input_file()
    coder.close()
