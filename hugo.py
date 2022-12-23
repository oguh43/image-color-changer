import png

import numpy as np

from math import sqrt
from PIL import Image
from collections import Counter

print("BEWARE, picture must have an alpha channel. If it does not, open gimp, Layer->Transparency->Add alpha channel. Than export and try again.")
delta = int(input("Collor defference delta? Recommended: 50> "))
numC = int(input("Number of colors? Recommended: 16> "))
fName = input("File name? (with .png)> ")

# Read and parse pixel data
file = open(fName,"rb")
reader = png.Reader(file=file)

data = [list(x) for x in list(reader.read()[2])]
file.seek(0)
width = png.Reader(file=file).read()[0]
file.close()

# Group pixel colors into 4
data = [x[i:i+4] for x in data for i in range(0,len(x)-3,4)]

# Convert to string and count (Counter can't count lists :(()
countable = [",".join(list(map(str, x))) for x in data]
counted = Counter(countable)

# Find the top 16 colors used
top = []
while len(top) != numC:
    # If we do not have 16 colors by the time we go through the counter, refresh it and lower the delta
    if counted == {}:
        counted = Counter(countable)
        delta -= 10
    mx = max(counted.values())
    key = list(counted.keys())[list(counted.values()).index(mx)]
    # Calculate current colors discance from all other top colors
    md = []
    for col in top:
        clr = list(map(int,key.split(",")))
        md.append(sqrt((col[0]-clr[0])**2 + (col[1]-clr[1])**2 + (col[2]-clr[2])**2))

    # If the delta is lower than 50, discard the color, else save it as another top color. Possible improvement, take into account max(md), as the collor could be very different from others and override the min check.
    
    if md != []:
        if min(md) < delta:
            del counted[key]
            continue
    top.append(list(map(int,key.split(","))))
    del counted[key]

# Construct the new image

new = []
dist = []
for pixel in data:
    # Calculate the color distance from all top colors
    for color in top:
        dist.append(sqrt((color[0]-pixel[0])**2 + (color[1]-pixel[1])**2 + (color[2]-pixel[2])**2))
    # Choose the best one and use it instead of the original color.
    best = dist.index(min(dist))
    new.append(top[best])
    dist = []

# Discard the alpha channel
new = [x[:3] for x in new]

# Regroup into 2d array, width-height
grouped = [new[i:i+width] for i in range(0,len(new)-width+1,width)]

# Save
array = np.array(grouped, dtype=np.uint8)
new_image = Image.fromarray(array)
new_image.save('new.png')
