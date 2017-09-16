import os, sys, fnmatch
from PIL import Image

size = 42, 42
matches = []

for root, dirnames, filenames in os.walk(sys.argv[1]):
    for filename in fnmatch.filter(filenames, '*.jpg'):
        matches.append(os.path.join(root, filename))
print matches

for infile in matches:
    outfile = os.path.splitext(infile)[0] + "_thumbnail.jpg"
    if infile != outfile:
        try:
            im = Image.open(infile)
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(outfile, "JPEG")
        except IOError:
            print "Cannot create thumbnail for '%s'" % infile

"""
    This script only resize jpg images to a samller one. 
    This script should be used into your environment used for the django project. 
    If you dont have PIL installed you can do: pip install image or easy_install PIL

    To use this script: 
        python image_resize.py C:\Users\ORDENADOR_1\Desktop\sharing_things\mediafiles\posts
"""