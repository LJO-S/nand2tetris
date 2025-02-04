
class Code:
    #------------------------------------------------------
    def __init__(self):
        self.comp_dict = {
            ("0",)         : "101010",
            ("1",)         : "111111",
            ("-1",)        : "111010",
            ("D",)         : "001100",
            ("A","M")      : "110000",
            ("!D",)        : "001101",
            ("!A", "!M")   : "110001",
            ("-D",)        : "001111",
            ("-A", "-M")   : "110011",
            ("D+1",)       : "011111",
            ("A+1","M+1")  : "110111",
            ("D-1",)       : "001110",
            ("A-1", "M-1") : "110010",
            ("D+A", "D+M") : "000010",
            ("D-A", "D-M") : "010011",
            ("A-D", "M-D") : "000111",
            ("D&A", "D&M") : "000000",
            ("D|A", "D|M") : "010101"
        }
        self.jmp_dict = {
            "null" : "000",
            "JGT" : "001",
            "JEQ" : "010",
            "JGE" : "011",
            "JLT" : "100",
            "JNE" : "101",
            "JLE" : "110",
            "JMP" : "111"
        }
    #------------------------------------------------------
    def __str__(self):
        pass
    #------------------------------------------------------
    def dest(self, dest_mnemonic):
        dest_binary = ['0','0','0']
        options = ['A', 'D', 'M']
        for ii in range(0,len(options)):
            if options[ii] in dest_mnemonic:
                dest_binary[ii] = '1'
        return ''.join(dest_binary)
    #------------------------------------------------------
    def comp(self, comp_mnemonic):
        comp_binary=[]
        if 'M' in comp_mnemonic:
            # then (a=1)
            comp_binary.append('1')
        else:
            # then (a=0)
            comp_binary.append('0')
        for key_group, binary in self.comp_dict.items():
            if comp_mnemonic in key_group:
                comp_binary.append(binary)
        return ''.join(comp_binary)
    #------------------------------------------------------

    def jump(self, jump_mnemonic):
        return self.jmp_dict[jump_mnemonic]

if __name__ == "__main__":
    code = Code()
    #print(code.dest("D"))
    print(code.jump("JLT"))
    