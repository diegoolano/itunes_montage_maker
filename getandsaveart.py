#!/usr/bin/python
import eyeD3
import os

class GetSaveArt:

	#sample usage:  python getandsaveart.py > output.txt
	#IMPORTANT CHANGE THESE TWO VARIBLES TO REFLECT WHERE YOUR ITUNES LIBRARY IS AND WHERE YOU WANT TO SAVE THE IMAGES FROM IT
	path_to_itunes = "/Users/diego/Music/iTunes/iTunes Music/"
	save_path = "/Users/diego/htdocs/itunesmontage/images/"
	song_counter = 1

	def getAndSaveCoverartImage(self, srcfile, new_name):
		#srcfile = location.replace("\ "," ")
		dstfolder = os.path.dirname(self.save_path) 
		#dstfile = self.save_path.replace(os.path.dirname(self.save_path)+"/","")
		
		tag = eyeD3.Tag()
		#print "src: %s, dstfolder: %s " % (srcfile, dstfolder )	
		if os.path.isfile(srcfile):
		    #print "%s is file" % srcfile
		    if os.path.splitext(srcfile)[1] == ".mp3":
			# Extract picture
			#print "% is mp3"
			try:
			    tag.link(srcfile)
			    for image in tag.getImages():
                                dstfile = "%s.JPEG" % new_name
				print "FILE %s: %s" % ( self.song_counter, dstfile )
				image.writeFile(dstfolder, dstfile)
				self.song_counter = self.song_counter + 1
	
			except:
			    print "Unable to extract image for: " + srcfile
			    #traceback.print_exc()
		else:
		    print "ERROR: %s not found to be file" % srcfile

	def traverseArtistAlbums(self):
		#starting from iTunes Music folder for each artist, 
		
		for artist in os.listdir(self.path_to_itunes):
			#for each artist
			artist_path = "%s%s" % (self.path_to_itunes, artist)
			if os.path.isdir(artist_path):
				for album in os.listdir(artist_path):
					#for each album, 
					album_path = "%s/%s" % ( artist_path, album)
					found_song = 0
					if os.path.isdir(album_path):
						for song in os.listdir(album_path):
							if found_song == 0:
								song_file = "%s/%s" % ( album_path, song)
								if os.path.splitext(song_file)[1] == ".mp3":
									#select first song for artwork and try to get/save art 		
									new_name = "%s-%s" % (artist,album)
									new_name = new_name.lower().replace(" ","_")
									print "saving %s to %s" % (song_file,new_name)
									self.getAndSaveCoverartImage(song_file,new_name)
									found_song = 1

				
if __name__ == '__main__':
    cl = GetSaveArt()
    cl.traverseArtistAlbums()

