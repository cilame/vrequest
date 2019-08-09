# brainfuck 和 ook 的核心算法相同，共用一个脚本

# brainfuck
def evaluate(code:str):
    code = cleanup(list(code))
    bmap = buildbmap(code)
    cells, ptr, cellptr, ret = [0], 0, 0, []
    while ptr < len(code):
        cmd = code[ptr]
        if cmd == ">": 
            cellptr += 1
            if cellptr == len(cells): cells.append(0)
        if cmd == "<": cellptr = 0 if cellptr <= 0 else cellptr - 1
        if cmd == "+": cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0
        if cmd == "-": cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255
        if cmd == "[" and cells[cellptr] == 0: ptr = bmap[ptr]
        if cmd == "]" and cells[cellptr] != 0: ptr = bmap[ptr]
        if cmd == ",": cells[cellptr] = b'\xff'
        if cmd == ".": ret.append(chr(cells[cellptr]))
        ptr += 1
    return ''.join(ret)

def cleanup(code):
    return ''.join(filter(lambda x: x in '.,[]<>+-', code))

def buildbmap(code):
    _stack, bmap = [], {}
    for pos, cmd in enumerate(code):
        if cmd == "[": _stack.append(pos)
        if cmd == "]":
            start = _stack.pop()
            bmap[start] = pos
            bmap[pos] = start
    return bmap

import re
# ook! 
def parse_ook_to_brainfuckmap(string, abc=('!', '?', '.')):
    maps = {
        ('!', '?'): '[',
        ('?', '!'): ']',
        ('.', '.'): '+',
        ('!', '!'): '-',
        ('.', '?'): '>',
        ('?', '.'): '<',
        ('!', '.'): '.',
        ('.', '!'): ',',
    }
    a, b, c = [i if i not in r'$()*+.[]?\/^{}' else '\\'+i for i in abc]
    rexgep = '|'.join([a, b, c])
    v = re.findall(rexgep, string)
    r = []
    for i in zip(v[::2],v[1::2]):
        t = [j.replace(a[-1], '!')\
              .replace(b[-1], '?')\
              .replace(c[-1], '.') for j in i]
        t = tuple(t)
        r.append(maps.get(t))
    return ''.join(r)


if __name__ == '__main__':
    # 普通的 brainfuck
    s = '>+++++++++[<++++++++>-]<.>+++++++[<++++>-]<+.+++++++..+++.>>>++++++++[<++++>-]<.>>>++++++++++[<+++++++++>-]<---.<<<<.+++.------.--------.>>+.'
    print(evaluate(s))
    print()

    # ook 加密实际上使用三个种类的字符以长度为2的组合来对应 brainfuck 里面的八个字符，
    # 实际上里面的算法还是使用的 brainfuck 的算法
    s = 'Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook. Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook? Ook? Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook? Ook! Ook! Ook? Ook! Ook? Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook? Ook. Ook! Ook. Ook. Ook. Ook. Ook. Ook. Ook. Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook! Ook. Ook. Ook? Ook. Ook? Ook. Ook. Ook! Ook.'
    s = parse_ook_to_brainfuckmap(s)
    print(s)
    print(evaluate(s))
    s = '''..... ..... ..... ..... !?!!. ?.... ..... ..... ..... .?.?! .?... .!...
..... ..... !.?.. ..... !?!!. ?!!!! !!?.? !.?!! !!!.. ..... ..... .!.?.
..... ...!? !!.?. ..... ..?.? !.?.. ..... .!.?. ..... ..... !?!!. ?!!!!
!!!!! !?.?! .?!.? ..... ....! ?!!.? ..... ...?. ?!.?. ..... !.?.. .....
!?!!. ?!!!! !!?.? !.?!! !!!!! !!!!. ..... ...!. ?.... ...!? !!.?. .....
?.?!. ?..!. ?.... ..... !?!!. ?!!!! !!!!? .?!.? !!!!! !!!!! !!!.? .....
..!?! !.?.. ....? .?!.? ....! .!!!. !!!!! !!!!! !!!!! !!.?. ..... .!?!!
.?... ...?. ?!.?. ..... !.!!! !!!!! !.?.. ..... ..!?! !.?.. ..... .?.?!
.?... ..... !.?.'''
    s = parse_ook_to_brainfuckmap(s)
    print(s)
    print(evaluate(s))
    print()