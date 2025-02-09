
class Parser:
    def __init__(self, path=None):
        self.file = self.open_input_file(path)
        self.current_command = None
        self.translation_table = dict.fromkeys(map(ord, ' @)('), None)

    def __str__(self):
        return f"{self.file}"

    def open_input_file(self, path):
        """Opens the file specified by path"""
        file = open(path, "r")
        return file
    
    def hasMoreCommands(self):
        """Checks if the current line is EOF or not
        but does not advance a line in the file. Skips
        comments and newlines."""
        pos = self.file.tell() # current position of file
        line = self.file.readline()
        line_split = line.split() 
        while line=='\n' or len(line_split)>0 and '//' in line_split[0]:
            pos = self.file.tell()
            line = self.file.readline()
            line_split = line.split()
        self.file.seek(pos) # go back to previous position
        if line:
            return True
        else:
            return False
    
    def advance(self):
        """Advances by reading the current line and 
        jumping to the next line"""
        self.current_command = self.file.readline() 

    def commandType(self):
        """Returns which command type the current command
        is."""
        if '@' in self.current_command:
            return "A_COMMAND"
        elif '=' in self.current_command or ';' in self.current_command:
            return "C_COMMAND"
        else:
            return "L_COMMAND"

    def symbol(self):
        """Returns the symbol. Uses the translation table 
        from __init__() to remove any @s, parentheses or 
        whitespace from the label or address command.
        Assumes A_COMMAND or L_COMMAND."""
        symbol = self.current_command.translate(self.translation_table)
        return symbol

    def dest(self):
        """Returns the dest mnemonic in the current C-command.
        We have 8 possibilities: A, M, D, AM, AD, MD, AMD, null"""
        dest = []
        if '=' in self.current_command:
            for letter in self.current_command:
                if letter == '=':
                    if 'A' in dest and 'M' in dest and 'D' in dest:
                        return "AMD"
                    elif 'A' in dest and 'D' in dest:
                        return "AD"
                    elif 'A' in dest and 'M' in dest:
                        return "AM"
                    elif 'M' in dest and 'D' in dest:
                        return "MD"
                    elif 'A' in dest:
                        return "A"
                    elif 'D' in dest:
                        return "D"
                    elif 'M' in dest:
                        return "M"
                else:
                    dest.append(letter)
        else:
            return "Null"

    def comp(self):
        # TODO: maybe we should actually allow dest=comp;jump
        """Returns the COMP mnemonic of the C_COMMAND.
        This assumes that we do not ahve something on the
        form of AMD=AMD;JMP"""
        comp = None
        j = 0
        if '=' in self.current_command:
            for letter in self.current_command:
                j += 1
                if letter == '=':
                    comp = self.current_command[j:]
                    return comp
        else:
            for letter in self.current_command:
                if letter == ';':
                    comp = self.current_command[:j]
                    return comp
                j += 1
        

    def jump(self):
        """Returns the JUMP mnemonic of the C_COMMAND."""
        jump = "null"
        j = 0
        if ';' in self.current_command:
            for letter in self.current_command:
                j += 1
                if letter == ';':
                    jump = self.current_command[j:]
        return jump

    def close_input_file(self):
        """Closes input file"""
        self.file.close()

    
if __name__ == "__main__":
    parser = Parser("rect/Rect.asm")
    i = 0
    while parser.hasMoreCommands() == True:
        parser.advance()
        if (
        parser.commandType() == "A_COMMAND" 
        or 
        parser.commandType() == "L_COMMAND"
        ):
            print(parser.symbol())
            #pass
        else:
            # C_COMMAND
            print(parser.dest())
            if parser.comp() == None:
                print(parser.jump())
            else:
                print(parser.comp())

    parser.close_input_file()