# modified from http://charlesleifer.com/blog/using-python-and-k-means-to-find-the-dominant-colors-in-images/

import cStringIO
import urllib
import os
from PIL import Image
from scipy.cluster import vq as sci
from numpy import array
import pytumblr
from pprint import pprint as pp

# fill this in first
target = ""
tumblr = pytumblr.TumblrRestClient(
	'',
	'',
	'',
	''
)

def get_points(img):
	points = []
	w, h = img.size
	for count, color in img.getcolors(w * h):
		points.append([color[0],color[1],color[2]])
	return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(img, n=3, trim=8):
	coords = [(x,y) for x in range(img.size[0]) for y in range(img.size[1])]
	
	for coord in coords:
		rgb = img.getpixel(coord)
		pix = (
			(rgb[0]//trim)*trim,
			(rgb[1]//trim)*trim,
			(rgb[2]//trim)*trim
		)
		img.putpixel(coord,pix)
	
	img.thumbnail((200, 200))
	w, h = img.size

	points = array(get_points(img))
	clusters = sci.kmeans(points, n)[0]
	rgbs = [map(int, c) for c in clusters]
	
	return map(rtoh, rgbs)

def main():
	info = tumblr.blog_info(target)
	posts = info["blog"]["posts"]
	step = 10
	colormap = {}

	for offset in range(0, posts, step):
		print("{0} - {1}".format(offset,offset+step))
		posts = tumblr.posts(target,limit=step,offset=offset)["posts"]
		for post in posts:
			if post["type"] == u'photo':
				for photo in post["photos"]:
					try:
						url = photo["original_size"]["url"]
						f = cStringIO.StringIO(urllib.urlopen(url).read())
						img = Image.open(f)
						colors = colorz(img,trim=32)
						print(url, colors)

						for color in colors:
							colormap[color] = colormap.get(color,0) + 1
					except:
						continue
		pp(colormap)

if __name__ == "__main__":
	main()
