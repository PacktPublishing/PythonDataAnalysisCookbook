import exifread
import pprint

f = open('covers.jpg', 'rb')

# Return Exif tags
tags = exifread.process_file(f)
print(tags.keys())
pprint.pprint(tags)
f.close()
