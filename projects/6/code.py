
class Code:
    def __init__(self):
        pass

    def __str__(self):
        pass

    def dest(self, dest_mnemonic):
        dest_binary = ['0','0','0']
        options = ['A', 'D', 'M']
        for ii in range(0,len(options)):
            if options[ii] in dest_mnemonic:
                dest_binary[ii] = '1'
        return ''.join(dest_binary)

    def comp(self):
        pass

    def jump(self):
        pass

if __name__ == "__main__":
    code = Code()
    print(code.dest("D"))