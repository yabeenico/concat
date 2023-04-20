#!/usr/bin/env python3
import sys
from lark import Lark
from lark import Transformer
from functools import reduce

# https://www.asciiart.eu/animals/cats

grammar = '''
concat    :  cat | ball | container | brace | paren | adjacent | multiple | over | group
group      :  "<" concat ">"
over      :  concat [ "/" concat ]
multiple  :  concat "*" /[0-9]+/
adjacent  :  concat [ "+" concat ]
paren     :  "(" [ concat ] ")"
brace     :  "{" [ concat ] "}"
container :  "[" [ concat ] "]"
ball      :  "ball"
cat       :  "cat"
%import common.WS
%ignore WS
'''

class T(Transformer):
    def concat(self, tree):
        return tree

    def group(self, tree): # <>
        return tree[0][0]

    def over(self, tree): # /
        at = tree[0][0].split('\n'); wt = len(at[0])
        ab = tree[1][0].split('\n'); wb = len(ab[0])
        at = list(map(lambda x: (x + ' ' * (wb - wt)), at))
        ab = list(map(lambda x: (x + ' ' * (wt - wb)), ab))
        return '\n'.join(at + ab)

    def multiple(self, tree): # *
        l = tree[0] * int(tree[1])
        return reduce(lambda x, y: self.adjacent([[x], [y]]), l)

    def adjacent(self, tree): # +
        al = tree[0][0].split('\n'); wl = len(al[0]); hl = len(al)
        ar = tree[1][0].split('\n'); wr = len(ar[0]); hr = len(ar)
        al = ([' ' * wl] * (hr - hl)) + al
        ar = ([' ' * wr] * (hl - hr)) + ar
        a = list(map(' '.join, zip(al, ar)))
        return '\n'.join(a)

    def paren(self, tree): # ()
        a = tree[0][0].split('\n') if len(tree) else [' ' * 8] * 4
        w = len(a[0])
        a.insert(0, '  ' + ('~' * w) + '  ') # 0
        a.append(   '  ' + ('~' * w) + '  ') # -1
        a[ 1] = ' (' + a[ 1] + ') '
        a[2:-2] = map(lambda x: f'( {x} )', a[2:-2])
        a[-2] = ' (' + a[-2] + ') '
        return '\n'.join(a)
        '''
          ~~~~~~~~    0
         ( /\    /)   1
        ( (' )  (  )  2:-2
        (  (  \  ) )  2:-2
         ( |(__)/ )  -2
          ~~~~~~~~   -1
        '''


    def brace(self, tree): # {}
        a = tree[0][0].split('\n') if len(tree) else [' ' * 8] * 4
        w = len(a[0])
        a.insert(0, '  ' + ('-' * w) + '  ') # 0
        a.append('  \\' + ('_' * (w - 1)) + '/ ') # -1
        a[1] = ' /' + a[1] + '\\ '
        a[2] = '/ ' + a[2] + ' |'
        a[3:-2] = map(lambda x: f'| {x} |', a[3:-2])
        a[-2] = ' \\' + a[-2] + ' |'
        return '\n'.join(a)
        '''
          ________    0
         / /\    /\   1
        / (' )  (  |  2
        |  (  \  ) |  3:-2
         \ |(__)// | -2
          \_______/  -1
        '''

    def container(self, tree): # []
        a = tree[0][0].split('\n') if len(tree) else [' ' * 8] * 4
        w = len(a[0])
        a = list(map(lambda x: f'|{x}|', a))
        a.insert(0, ' ' + '-' * w + ' ')
        a.append(   ' ' + '-' * w + ' ')
        return '\n'.join(a)

    def ball(self, tree):
        return \
            "        \n" + \
            "        \n" + \
            "   __   \n" + \
            " _/  \_@"

    def cat(self, tree):
        return \
            " /\    /\n" + \
            "(' )  ( \n" + \
            " (  \  )\n" + \
            " |(__)/ "

def main():
    text = sys.argv[1]
    parser = Lark(grammar, start='concat')
    tree = parser.parse(text)
    #print(tree.pretty()) # debug
    result = T().transform(tree)[0]
    print(result)

if __name__ == '__main__':
    main()

