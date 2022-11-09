#!/usr/bin/python3

#requirements
from PIL import Image
import math


def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(bin(i))
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
		for k in i:
			[r,g,b]=im1.getpixel((x,y))
			r = r - int(k, 2)
			print(r)
			value = (r,g,b)
			im1.putpixel((x,y), value)
print(r,g,b)
im1.save('new.jpg')
im2 = Image.open('new.jpg')
img = im2.load()
[xxs,yys] = im2.size
for x in range(0,xs):
	for y in range (0,ys):
		for xx in range(0,xxs):
			for yy in range (0,yys):
				[r,g,b]=im1.getpixel((x,y))
				[r2,g2,b2]=im2.getpixel((xx,yy))
				k= r -r2
				print(bin(k))
