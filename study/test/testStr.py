import sys

sys.path.append('..')
a = 'hhh%s' % 'aaa'
print(a)

b = 'h%sh%sh%s' % ('a','a','a')
print(b)

c = 'h%(aa)sh%(bb)sh%(cc)s' % {'aa':'aa','bb':'bb','cc':'cc'}
print(c)

d = 'j{}j{}'.format('d','d')
print(d)

a = 14000 + 275 + 150 + 255 + 600
print a
b = 336 + 21 + 1680 + 15 + 84 + 235.77

print b

print a-b