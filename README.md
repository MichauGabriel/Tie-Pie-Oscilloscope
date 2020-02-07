# Tie Pie Oscilloscope
 Python code to read '.tps' binary files
 
 The function takes as input an opened file (`fileID`) so that if you can use it, among others, with the zipfile packages:
 
 ```
 import readtps as rtps
 import zipfile
 
 zfile = zipfile.ZipFile('mayArchive.zip')
 filenames = [e for e in zfile.infolist() if '.tps' in e.filename]
 for file in filenames:
	fileID = zfile.open(file, "r")
	data, fsr, chRange = rtps.readTPS(fileID)
```
 or 
```
 fileID = open('myfile.tps', "rb")
```

This is exploratory work, in all the tps file I dealt with, the data was always in float32 but this is maybe encoded in the 'FMT' key.
In all the experiements I did, I had all channels with the same settings, in particular sampling frequency and length. This might not always be the case.
