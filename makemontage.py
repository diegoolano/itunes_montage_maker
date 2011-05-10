#!/usr/bin/python
import os
from PIL import Image
import sys
import math

class MakeMontage:
  
  #SET THIS PATH TO LOCATION OF CONSOLIDATED IMAGES FOLDER
  path_to_image = "/Users/diego/htdocs/itunesmontage/images/"
  
  #SAMPLE USAGE:
  #1) to see what the distribution of your images look like, in the main method below uncomment out 
  	#mk.get_dimensions()
  #   and run python makemontage.py > imagedistribution.txt

  #2) to resize all images to a certain a size uncomment out only
  	#mk.make_thumbs(200)
  #   and run python makemontage.py .. if you would rather a different size than 200x200, you'll need to create a folder in images/ named thumbs_SIZE and then change the 200 from the above mk.make_thumbs line to SIZE

  #3) to then make the montage image, uncomment only the following	
  	#mk.make_montage(200)
  #   and pass whatever SIZE you used in step 2.
  #  IMPORTANT: this final method is severly lacking, but easy to adapt if you want to save images of a different name or change the dimensions of the output.

  def get_dimensions(self):
	highest = 0
	highest_img = ''
	shortest = 10000
	shortest_img = ''

	widest = 0
	widest_img = ''    
	skinniest = 10000
	skinniest_img = ''    

	cumalative_height = 0
	cumalative_width = 0
	counter = 0
	ts_limit = 200
	too_small = 0
	ts_array = {}
	for img in os.listdir(self.path_to_image):
		if os.path.splitext(img)[1] == ".JPEG":
			full_img = "%s%s" % ( self.path_to_image, img)
			print "full: %s" % full_img
			try:
				pimg = Image.open(full_img)
				if pimg.size[1] > highest:
				     highest = pimg.size[1]
				     highest_img = img
				if pimg.size[0] < shortest:
				     shortest = pimg.size[1]
				     shortest_img = img
				if pimg.size[0] > widest:
				     widest = pimg.size[0]
				     widest_img = img
				if pimg.size[0] < skinniest:
				     skinniest = pimg.size[0]
				     skinniest_img = img
				cumalative_height += pimg.size[1]
				cumalative_width += pimg.size[0]
				counter = counter + 1
				if pimg.size[0] < ts_limit or pimg.size[1] < ts_limit:
					too_small = too_small + 1
					ts_array[img] = "%s x %s" % (pimg.size[0], pimg.size[1])
				
			except:
				print "ERROR reading: %s" % full_img

	print "HighestImg: %s - %s\n ShortestImg: %s-%s" % (highest_img, highest, shortest_img, shortest)
	print "WidestImg: %s - %s\n SkinniestImg: %s-%s" % ( widest_img, widest, skinniest_img, skinniest)
	print "Avg Height: %s\n Avg Width: %s" % (cumalative_height / counter, cumalative_width/counter)
	print "Total: %s" % counter
	print "Too small: %s" % too_small
	for i in ts_array:
		print "%s (%s)" % (i,ts_array[i])

  def make_thumbs(self,size):
	local_counter = 0
	error_counter = 0
	for img in os.listdir(self.path_to_image):
		if os.path.splitext(img)[1] == ".JPEG":
			full_img = "%s%s" % ( self.path_to_image, img)
			try:
				pimg = Image.open(full_img)
				if pimg.size[0] < size or pimg.size[1] < size:
					print "Error image too small: skipping %s" % img
					error_counter = error_counter + 1
				else:
					outfolder = "%sthumbs_%s/" % (self.path_to_image, size)
					if not os.path.isdir(outfolder):	     
						os.mkdir( outfolder, 777)
					outfile = "%s%s" % ( outfolder, img)
					print "Saving: %s" % outfile
					pimg.thumbnail((size,size))				
					pimg.save(outfile, "JPEG")
					local_counter = local_counter + 1
			except:
				print "Error reading file skipping: %s" % full_img
				error_counter = error_counter + 1
	print "Local counter: %s\n Error counter %s" % ( local_counter, error_counter )

  def make_montage(self,size):
	desired_width = 23 * 200 #1400
	thumbs_folder = "%sthumbs_%s/" % ( self.path_to_image, size )
	totalcount = 534	
	per_row = 23 #1400 / size
	height = math.ceil(float(totalcount) / float(per_row)) * size
	output_image = Image.new("RGBA", (desired_width, int(height)))
		
	xval = 0
	yval = 0
	for img in os.listdir(thumbs_folder):
		if os.path.splitext(img)[1] == ".JPEG":
			try:
				full_img = "%s%s" % ( thumbs_folder, img )
                                pimg = Image.open(full_img)
				output_image.paste(pimg, (xval, yval * size ))
			
				xval = xval + size
				if xval >= desired_width:
					xval = 0
					yval = yval + 1
			except:	
				print "Error reading file skipping: %s" % full_img
	
	outfile = "%s%s" % (thumbs_folder, "Montage-WIDE.JPEG")
	print "Saving Montage %s" % outfile
	output_image.save(outfile,"JPEG")

if __name__ == '__main__':
  mk = MakeMontage()
  #mk.get_dimensions()
  #mk.make_thumbs(200)
  #mk.make_montage(200)
