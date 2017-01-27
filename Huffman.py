import heapq
from collections import namedtuple, Counter


class Node(namedtuple('Node', ['left', 'right'])):
    def walk(self, code, acc):
        self.left.walk(code, acc + '0')
        self.right.walk(code, acc + '1')


class Leaf(namedtuple('Leaf', ['char'])):
    def walk(self, code, acc):
        code[self.char] = acc or '0'


def huffman_encode(string):
    h = []
    for char, freq in Counter(string).items():
        h.append((freq, len(h), Leaf(char)))

    tmp = []
    for i in range(len(sorted(h))):
        tmp.append([h[i][0], h[i][2][0]])

    tmp.sort(key=lambda x: x[0], reverse=True)
    for item in tmp:
        print item[0], item[1]

    print '\n'

    heapq.heapify(h)
    count = len(h)

    while len(h) > 1:
        cur_freq, _cur_count, left = heapq.heappop(h)
        next_freq, _next_count, right = heapq.heappop(h)

        heapq.heappush(h, (cur_freq+next_freq, count, Node(left, right)))
        count += 1


    code = {}
    if h:
        [(_freq, _count, root)] = h
        root.walk(code, '')
        # parse_tree(root)

    return code


def parse_tree(tree, cnt=0, side=''):
    if isinstance(tree, Node):
        parse_tree(tree.left, cnt+1, 'left')
        parse_tree(tree.right, cnt+1, 'right')
    if isinstance(tree, Leaf):
        print '  ' * cnt, side + ' ' + tree.char


def huffman_decode(encoded, code):
    sx = []
    enc_ch = ""
    for ch in encoded:
        enc_ch += ch
        for dec_ch in code:
            if code.get(dec_ch) == enc_ch:
                sx.append(dec_ch)
                enc_ch = ""
                break
    return "".join(sx)


if __name__ == '__main__':
    fp = open('test.txt', 'r')
    string = fp.read()
    s = string.decode('utf-8')

    code = huffman_encode(s)
    encoded = ''.join(code[ch] for ch in s)

    print(len(code), len(encoded))

    for ch in sorted(code, key=code.get):
        print ch + ':', code[ch]

    print '\n'
    print encoded

    output = open('encoded.bin', 'wb')

    tmp = []
    p = len(encoded) / 8
    for i in range(p):
        tmp.append(encoded[i:i+8])

    for elem in tmp:
        output.write(chr(int(elem, 2)))

    output.close()

    tt = "0x%x" % int(encoded, 2)
    print tt
    #
    re_tt = bin(int(tt, 16))[2:]
    print re_tt


    print '\n'

    decode = huffman_decode(encoded, code)
    print decode

    fp1 = open('test2.txt', 'w')
    fp1.write(decode.encode('utf-8'))
    fp1.close()




