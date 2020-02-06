# Tie Pie Oscilloscope
 Python code to read '.tps' binary files
 
 The function takes as input a fileID so that if you can use it with the zipfile packages:
 
 ```
 import readtps as rtps
 import zipfile
 
 zfile = zipfile.ZipFile(archive)
 filenames = [e for e in zfile.infolist() if '.tps' in e.filename]
 for file in filenames:
	fileID = zfile.open(file, "r")
	data, fsr, chRange = rtps.readTPS(fileID)
```
 or 
```
 fileID = open('myfile.tps', "rb")
```
