import urllib2
import xml.etree.ElementTree as et
import os
import string

uname = raw_input("Lastfm username: ")

# Download the xml data
xmlurl = ('http://ws.audioscrobbler.com/2.0/user/%s/podcast.rss' % uname)
xmlresponse = urllib2.urlopen(xmlurl)
xmlstring = xmlresponse.read()

# Build it into an xml object
xml = et.XML(xmlstring)

def makesafe(filename):
  validchars = "-_.() %s%s" % (string.ascii_letters, string.digits)
  return ''.join(c for c in filename if c in validchars)


for item in xml[0].findall('item'):
  # Grab the artist string and url
  songtitle = makesafe(item[0].text)
  artistname = makesafe(item[2].text)
  fileurl = item[3].get('url')
  filename = fileurl.split('/')[-1]
  # Let the user know what's going on
  print ('Downloading %s - %s from %s' % (artistname, songtitle, fileurl))
  # make a directory for the artist if it doesn't exist
  if not os.path.exists(artistname): 
    os.mkdir(artistname)
  # download the file (only if it's not there already)
  filepath = artistname + '/' + filename
  if not os.path.exists(filepath):
    try:
      mp3file = urllib2.urlopen(fileurl)
      fileoutput =  open(filepath, 'wb')
      fileoutput.write(mp3file.read())
      fileoutput.close()
    except:
      print "Download failed, skipping file"
      continue



