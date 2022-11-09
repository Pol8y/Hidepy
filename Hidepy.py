#!/usr/bin/python3

#requirements
from PIL import Image
import math


def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  return m


inp = input('Write the sentence you want to hide:\n')
i=toBinary(inp)
print(' '.join(map(str, i)))
inp2 = input('where\'s the image you want to hide your secret into?\n')
im1 = Image.open(inp2)
img = im1.load()
[xs,ys]=im1.size
print(xs,ys)
for x in range(0,xs):
	for y in range (0,ys):
		[r,g,b]=im1.getpixel((x,y))
		r = r -250
		g = g -250
		b = b -250
		R = bin(255)[2:]
		value = (r,g,b)
		im1.putpixel((x,y), value)
print(r,g,b,R)
im1.save('new.jpg')
