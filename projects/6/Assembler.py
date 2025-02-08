from coder import Code
from parser import Parser
from symbolTable import SymbolTable
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

    # 1st pass
    parser_1P = Parser(input_path)
    # 2nd pass
    parser_2P = Parser(input_path)

    coder = Code()
    symbolTable = SymbolTable()

    secondPass = False
    breakLoop = False
    
    while breakLoop == False:
        if secondPass == False:
            # Only handle labels here (XXX)
            i = 0
            while parser_1P.hasMoreCommands() == True:
                parser_1P.advance()
                if ((parser_1P.commandType() == "A_COMMAND") or
                    (parser_1P.commandType() == "C_COMMAND")):
                    # A_COMMAND
                    i += 1
                else:
                    # L_COMMAND
                    # Check if the command is in hash table
                    if not symbolTable.contains(parser_1P.symbol()):
                        symbolTable.addEntry(parser_1P.symbol(), i)
            parser_1P.close_input_file()
            secondPass = True
        else:
            # Normal pass, but we also handle variables @XXX
            i = 0
            while parser_2P.hasMoreCommands() == True:
                parser_2P.advance()
                if (parser_2P.commandType() == "A_COMMAND" ):
                    if symbolTable.contains(parser_2P.symbol()):
                        # This is a label or prev encountered variable
                        addr = symbolTable.getAddress(parser_2P.symbol())
                        output = "0" + '{0:015b}'.format(int(addr))
                    elif parser_2P.symbol().strip().isdigit():
                        output = "0" + '{0:015b}'.format(int(parser_2P.symbol()))
                    else:
                        # First encounter
                        symbolTable.addEntry(parser_2P.symbol(), 16+i)
                        output = "0" + '{0:015b}'.format(int(16+i))
                        i += 1
                    print(output)
                elif (parser_2P.commandType() == "C_COMMAND"):
                    # C = 111 + comp + dest + jump
                    dest = parser_2P.dest()
                    comp = parser_2P.comp()
                    jump = parser_2P.jump()
                    output = "111" + coder.comp(comp) + coder.dest(dest) + coder.jump(jump)
                    print(output) 
            parser_2P.close_input_file()
            breakLoop = True
            

    



    