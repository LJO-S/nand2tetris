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


class Code:

    def __init__(self, path=None):
        self.file = self.open_output_file(path)
        self.stack = []
        self.sp = 256
        self.fileName = None

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
        if command == "add":
            self.sp_decr()
            self.file.write("@" + str(self.sp) + "\n" + "D=M" + "\n")
            self.file.write("@" + str(self.sp - 1) + "\n" + "M=M+D" + "\n")
        elif command == "sub":
            pass
        elif command == "neg":
            pass
        elif command == "eq":
            pass
        elif command == "gt":
            pass
        elif command == "lt":
            pass
        elif command == "and":
            pass
        elif command == "or":
            pass
        else:
            # not
            pass

    def writePushPop(self, command: str, segment: str, index: int):
        # börja med Push
        # self.sp är vår address-skrivare. När ska RAM[0] uppdateras? Hela tiden?
        if command == "C_PUSH":
            if segment == "constant":
                self.file.write("@" + str(index) + "\n" + "D=A" + "\n")
                self.file.write("@" + str(self.sp) + "\n" + "M=D" + "\n")
            else:
                pass
        else:
            # pop
            pass
        self.sp_incr()

    def sp_incr(self):
        self.sp += 1
        self.sp_write()

    def sp_decr(self):
        self.sp -= 1
        self.sp_write()

    def sp_write(self):
        self.file.write("@" + str(self.sp) + "\n" + "D=A" + "\n")
        self.file.write("@SP" + "\n" + "M=D" + "\n")

    def close(self):
        """Closes output file"""
        self.file.close()


if __name__ == "__main__":
    pass
