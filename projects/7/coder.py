# börja med StackArithmetic
#
# PUSH
# stack[sp] = x
# sp += 1

# push "segment" "idx" trycker segment[idx] upp på stacken

# POP
# sp -= 1
# x = stack[sp]

# pop "segment" "idx" tar översta stackvärdet och storar i segment[idx]

# True = -1 = 0xFFFF
# False = 0 = 0x0000

# Lägg tid på att fatta hur fan man i .asm
# skapar add, sub, neg, eq, gt, lt, and, or, not

# RAM usage
# 0: SP, 1: LOCAL base pntr, 2: ARG base pntr, 3: THIS base pntr, 4: THAT base pntr, 5-12: temp, 13-15: null
# 16-255: static
# 256-2047: STACK
# 2048-16483: heap

# TODO list
# 1. Replace all self.sp with actual @SP operations
# 2. Fix main.py to actually output files with the directory name
#
#


class Code:

    def __init__(self, path=None):
        self.file = self.open_output_file(path)
        self.stack = []
        self.sp = 256
        self.fileName = None
        self.i = 0  # iterator

    def open_output_file(self, path: str):
        """Opens the file specified by path"""
        file = open(path, "w")
        return file

    def setFileName(self, fileName: str):
        # Should reset accordingly

        # varje fil ska ha en egen static
        # en variable i en fil kan då få namnet fileName.variable till @
        self.fileName = fileName
        pass

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
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=M+D" + "\n")
        elif command == "sub":
            self.file.write("// sub" + "\n")
            self.sp_decr()
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=M-D" + "\n")
        elif command == "neg":
            # -y
            self.file.write("// NEG " + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=-M" + "\n")
        elif command == "eq":
            # x = y
            self.file.write("// X = Y" + "\n")
            self.sp_decr()
            # {fill with false} @skip_x_True 0;JMP
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "D=D-M" + "\n")
            self.file.write("@x_True." + str(self.i) + "\n" + "D;JEQ" + "\n")
            # false
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=0" + "\n")
            self.file.write("@cont." + str(self.i) + "\n" + "0;JMP" + "\n")
            # true
            self.file.write("(x_True." + str(self.i) + ")" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=-1" + "\n")
            # continue
            self.file.write("(cont." + str(self.i) + ")" + "\n")
            # incr internal label counter
            self.i += 1
        elif command == "gt":
            # x > y
            self.file.write("// X > Y" + "\n")
            self.sp_decr()
            # {fill with false} @skip_x_True 0;JMP
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "D=D-M" + "\n")
            self.file.write("@x_True." + str(self.i) + "\n" + "D;JLT" + "\n")
            # false
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=0" + "\n")
            self.file.write("@cont." + str(self.i) + "\n" + "0;JMP" + "\n")
            # true
            self.file.write("(x_True." + str(self.i) + ")" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=-1" + "\n")
            # continue
            self.file.write("(cont." + str(self.i) + ")" + "\n")
            # incr internal label counter
            self.i += 1
        elif command == "lt":
            # x < y
            self.file.write("// X < Y" + "\n")
            self.sp_decr()
            # {fill with false} @skip_x_True 0;JMP
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "D=D-M" + "\n")
            self.file.write("@x_True." + str(self.i) + "\n" + "D;JGT" + "\n")
            # false
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=0" + "\n")
            self.file.write("@cont." + str(self.i) + "\n" + "0;JMP" + "\n")
            # true
            self.file.write("(x_True." + str(self.i) + ")" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=-1" + "\n")
            # continue
            self.file.write("(cont." + str(self.i) + ")" + "\n")
            # incr internal label counter
            self.i += 1
        elif command == "and":
            # x And y
            self.file.write("// x & y" + "\n")
            self.sp_decr()
            # acquire Y
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            # & operation on X
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=D&M" + "\n")
        elif command == "or":
            # x Or y
            self.sp_decr()
            self.file.write("// x | y" + "\n")
            # acquire Y
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            # | operation on X
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=D|M" + "\n")
        else:
            # Not y
            self.file.write("// !Y" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=!M" + "\n")

    def writePushPop(self, command: str, segment: str, index: int):
        if command == "C_PUSH":
            self.file.write("// push " + str(segment) + " " + str(index) + "\n")
            if segment == "constant":
                self.file.write("@" + str(index) + "\n" + "D=A" + "\n")
            elif segment == "temp":
                self.file.write("@R" + str(5 + int(index)) + "\n")
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
                elif segment == "pointer":
                    pass  # TODO
                else:
                    raise Exception("Somehow C_PUSH but unknown segment")
                self.file.write("A=M" + "\n")
                for _ in range(int(index)):
                    self.file.write("A=A+1" + "\n")
                self.file.write("D=M" + "\n")
            self.file.write("@" + str(self.sp) + "\n" + "M=D" + "\n")
            self.sp_incr()

        elif command == "C_POP":
            self.file.write("// pop " + str(segment) + " " + str(index) + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "D=M" + "\n")
            if segment == "temp":
                self.file.write("@R" + str(5 + int(index)) + "\n")
            else:
                if segment == "local":
                    self.file.write("@LCL" + "\n")
                elif segment == "argument":
                    self.file.write("@ARG" + "\n")
                elif segment == "this":
                    self.file.write("@THIS" + "\n")
                elif segment == "that":
                    self.file.write("@THAT" + "\n")
                elif segment == "static":
                    pass  # TODO
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

    def sp_write(self):
        """SP INCR/DECR helper function"""
        self.file.write("@" + str(self.sp) + "\n" + "D=A" + "\n")
        self.file.write("@SP" + "\n" + "M=D" + "\n")

    def close(self):
        """Closes output file"""
        self.file.close()


if __name__ == "__main__":
    pass
