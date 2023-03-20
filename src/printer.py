import os

def printer(text, inpt=None):

    
    terminal_width = os.get_terminal_size().columns

    print("-" * terminal_width)
    print()
    if text is not None:
        print(text)
        # lines = ['{:^80}'.format(s) for s in text.split('\n')]
        # print('\n'.join(line.center(terminal_width) for line in lines))

    if inpt:
        # return input(inpt.rjust(terminal_width//2))
        return input(inpt)
    
    print()


test = printer("Hello World")

print(test)