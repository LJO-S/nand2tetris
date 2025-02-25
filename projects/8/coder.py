# True = -1 = 0xFFFF
# False = 0 = 0x0000

# RAM usage
# 0: SP, 1: LOCAL base pntr, 2: ARG base pntr, 3: THIS base pntr, 4: THAT base pntr, 5-12: temp, 13-15: null
# 16-255: static
# 256-2047: STACK
# 2048-16483: heap


class Code:

    def __init__(self, path=None):
        self.file = self.open_output_file(path)
        self.stack = []
        self.sp = 256
        self.fileName = None
        self.i = 0  # iterator
        self.call_iterator = 0

    def open_output_file(self, path: str):
        """Opens the file specified by path"""
        file = open(path, "w")
        return file

    def setFileName(self, fileName: str):
        # Should reset accordingly
        self.fileName = fileName

    def writeArithmetic(self, command: str):
        """Returns the .asm code corresponding
        to the input VM command"""
        # STACK
        # ..
        # x
        # y
        # .. <--- SP
        if command == "add":
            self.file.write("// add" + "\n")
            self.sp_decr()
            self.get_sp(0)
            self.file.write("D=M" + "\n")
            self.get_sp(-1)
            self.file.write("M=M+D" + "\n")
        elif command == "sub":
            self.file.write("// sub" + "\n")
            self.sp_decr()
            self.get_sp(0)
            self.file.write("D=M" + "\n")
            self.get_sp(-1)
            self.file.write("M=M-D" + "\n")
        elif command == "neg":
            # -y
            self.file.write("// NEG " + "\n")
            self.get_sp(-1)
            self.file.write("M=-M" + "\n")
        elif command == "eq":
            # x = y
            self.file.write("// X = Y" + "\n")
            self.sp_decr()
            # {fill with false} @skip_x_True 0;JMP
            self.get_sp(0)
            self.file.write("D=M" + "\n")
            self.get_sp(-1)
            self.file.write("D=D-M" + "\n")
            self.file.write("@x_True." + str(self.i) + "\n" + "D;JEQ" + "\n")
            # false
            self.get_sp(-1)
            self.file.write("M=0" + "\n")
            self.file.write("@cont." + str(self.i) + "\n" + "0;JMP" + "\n")
            # true
            self.file.write("(x_True." + str(self.i) + ")" + "\n")
            self.get_sp(-1)
            self.file.write("M=-1" + "\n")
            # continue
            self.file.write("(cont." + str(self.i) + ")" + "\n")
            # incr internal label counter
            self.i += 1
        elif command == "gt":
            # x > y
            self.file.write("// X > Y" + "\n")
            self.sp_decr()
            # {fill with false} @skip_x_True 0;JMP
            self.get_sp(0)
            self.file.write("D=M" + "\n")
            self.get_sp(-1)
            self.file.write("D=D-M" + "\n")
            self.file.write("@x_True." + str(self.i) + "\n" + "D;JLT" + "\n")
            # false
            self.get_sp(-1)
            self.file.write("M=0" + "\n")
            self.file.write("@cont." + str(self.i) + "\n" + "0;JMP" + "\n")
            # true
            self.file.write("(x_True." + str(self.i) + ")" + "\n")
            self.get_sp(-1)
            self.file.write("M=-1" + "\n")
            # continue
            self.file.write("(cont." + str(self.i) + ")" + "\n")
            # incr internal label counter
            self.i += 1
        elif command == "lt":
            # x < y
            self.file.write("// X < Y" + "\n")
            self.sp_decr()
            # {fill with false} @skip_x_True 0;JMP
            self.get_sp(0)
            self.file.write("D=M" + "\n")
            self.get_sp(-1)
            self.file.write("D=D-M" + "\n")
            self.file.write("@x_True." + str(self.i) + "\n" + "D;JGT" + "\n")
            # false
            self.get_sp(-1)
            self.file.write("M=0" + "\n")
            self.file.write("@cont." + str(self.i) + "\n" + "0;JMP" + "\n")
            # true
            self.file.write("(x_True." + str(self.i) + ")" + "\n")
            self.get_sp(-1)
            self.file.write("M=-1" + "\n")
            # continue
            self.file.write("(cont." + str(self.i) + ")" + "\n")
            # incr internal label counter
            self.i += 1
        elif command == "and":
            # x And y
            self.file.write("// x & y" + "\n")
            self.sp_decr()
            # acquire Y
            self.get_sp(0)
            self.file.write("D=M" + "\n")
            # & operation on X
            self.get_sp(-1)
            self.file.write("M=D&M" + "\n")
        elif command == "or":
            # x Or y
            self.sp_decr()
            self.file.write("// x | y" + "\n")
            # acquire Y
            self.get_sp(0)
            self.file.write("D=M" + "\n")
            # | operation on X
            self.get_sp(-1)
            self.file.write("M=D|M" + "\n")
        else:
            # Not y
            self.file.write("// !Y" + "\n")
            self.get_sp(-1)
            self.file.write("M=!M" + "\n")

    def writePushPop(self, command: str, segment: str, index: int):
        if command == "C_PUSH":
            self.file.write("// push " + str(segment) + " " + str(index) + "\n")
            if segment == "constant":
                self.file.write("@" + str(index) + "\n" + "D=A" + "\n")
            elif segment == "temp":
                self.file.write("@R" + str(5 + int(index)) + "\n")
                self.file.write("D=M" + "\n")
            elif segment == "pointer":
                if int(index) == 0:
                    self.file.write("@THIS" + "\n")
                elif int(index) == 1:
                    self.file.write("@THAT" + "\n")
                else:
                    raise Exception("Invalid pointer index: " + str(index))
                self.file.write("D=M" + "\n")
            elif segment == "static":
                self.file.write("@" + self.fileName + "." + str(index) + "\n")
                self.file.write("D=M" + "\n")
            else:
                if segment == "argument":
                    self.file.write("@ARG" + "\n")
                elif segment == "this":
                    self.file.write("@THIS" + "\n")
                elif segment == "that":
                    self.file.write("@THAT" + "\n")
                elif segment == "local":
                    self.file.write("@LCL" + "\n")
                else:
                    raise Exception("Somehow C_PUSH but unknown segment")
                self.file.write("A=M" + "\n")
                for _ in range(int(index)):
                    self.file.write("A=A+1" + "\n")
                self.file.write("D=M" + "\n")
            self.get_sp(0)
            self.file.write("M=D" + "\n")
            self.sp_incr()

        elif command == "C_POP":
            self.file.write("// pop " + str(segment) + " " + str(index) + "\n")
            self.get_sp(-1)
            self.file.write("D=M" + "\n")
            if segment == "temp":
                self.file.write("@R" + str(5 + int(index)) + "\n")
            elif segment == "pointer":
                if int(index) == 0:
                    self.file.write("@THIS" + "\n")
                elif int(index) == 1:
                    self.file.write("@THAT" + "\n")
                else:
                    raise Exception("Invalid pointer index: " + str(index))
            elif segment == "static":
                self.file.write("@" + self.fileName + "." + str(index) + "\n")
            else:
                if segment == "local":
                    self.file.write("@LCL" + "\n")
                elif segment == "argument":
                    self.file.write("@ARG" + "\n")
                elif segment == "this":
                    self.file.write("@THIS" + "\n")
                elif segment == "that":
                    self.file.write("@THAT" + "\n")
                else:
                    raise Exception("ERROR: somehow C_POP but unknown segment")
                self.file.write("A=M" + "\n")
                for _ in range(int(index)):
                    self.file.write("A=A+1" + "\n")
            # write data
            self.file.write("M=D" + "\n")
            self.sp_decr()
        else:
            raise Exception("Unknown command type: " + str(command) + "\n")

    def sp_incr(self):
        """Increment SP"""
        self.sp += 1
        self.file.write("@SP" + "\n" + "M=M+1" + "\n")

    def sp_decr(self):
        """Decrement SP"""
        self.sp -= 1
        self.file.write("@SP" + "\n" + "M=M-1" + "\n")

    def get_sp(self, index):
        """Get current SP"""
        self.file.write("@SP" + "\n" + "A=M" + "\n")
        if index < 0:
            for _ in range(abs(index)):
                self.file.write("A=A-1" + "\n")
        else:
            for _ in range(index):
                self.file.write("A=A+1" + "\n")

    def close(self):
        """Closes output file"""
        self.file.close()

    def writeInit(self):
        """Writes SP = 256"""
        self.file.write("@SP" + "\n" + "D=256" + "\n")

    def writeLabel(self, label: str):
        """Writes a label"""
        self.file.write(f"({label})" + "\n")

    def writeGoto(self, label: str):
        """Writes an unconditional JMP command"""
        self.file.write(f"@{label}" + "\n" + "0;JMP" + "\n")

    def writeIf(self, label: str):
        """Writes a conditional JMP command by
        checking the last stack value pushed.
        0x0000 = False , 0xFFFF = True"""
        self.get_sp(-1)  # Get last value of SP
        self.file.write(f"@{label}" + "\n")
        self.file.write(f"D;JNE" + "\n")  # execute if D != 0

    def writeCall(self, functionName: str, numArgs: int):
        # We need to maintain Global Stack structure when calling function:

        # 1. push return-address
        # 2. push LCL
        # 3. push ARG
        # 4. push THIS
        # 5. push THAT
        # 6. ARG = SP-n-5 (-5 due to pushing saved state of caller)
        # 7. LCL = SP
        # 8. goto f
        # 9. (return-address)

        # Save state of caller
        for loc in ["RETURN_ADDR_CALL", "LCL", "ARG", "THIS", "THAT"]:
            if loc == "RETURN_ADDR_CALL":
                self.file.write(f"@{loc}.{self.call_iterator}" + "\n")
                self.file.write("D=A" + "\n")
            else:
                self.file.write(f"@{loc}" + "\n" + "D=M" + "\n")
            self.get_sp(0)
            self.file.write("M=D" + "\n")
            self.sp_incr()

        # reposition ARG
        self.file.write("@SP" + "\n" + "D=M" + "\n")
        self.file.write("@ARG" + "\n" + "M=D" + "\n")
        for _ in range(numArgs + 5):  # +5 due to 5 pushes of saved caller state
            self.file.write("A=A-1" + "\n")

        # reposition LCL
        self.file.write("@SP" + "\n" + "D=M" + "\n")
        self.file.write("@LCL" + "\n" + "M=D" + "\n")

        # transfer ctrl (goto f, unconditionally)
        self.writeGoto(functionName)

        # Declare label for return-address??
        self.writeLabel("RETURN_ADDR_CALL." + str(self.call_iterator))

        # Increment whenever this function is called upon
        self.call_iterator += 1

    def writeReturn(self):
        # oof
        pass

    def writeFunction(self, functionName: str, numLocals: int):
        # TODO: use self.filename to name shit
        pass


if __name__ == "__main__":
    pass
