import re 
import datetime


sourceFile = open("OR Song Times.txt", "r")

print("okay")

parsedFile  = open('parsed_song_times.txt', 'w'); 
for line in sourceFile: 
    parsedData = line 
    # matchString = '(\d+-\d+)'
    if re.match( ".+(\d+-\d+).+", parsedData):
        seconds = re.search( '(\d+-\d+)', parsedData).group(0)   
        start, stop = seconds.split('-'); 
        tstart= str(datetime.timedelta(seconds=int(start)))
        tstop= str(datetime.timedelta(seconds=int(stop)))
        parsedData = parsedData.replace(seconds, f"{tstart}-{tstop}")


    parsedFile.write(parsedData)
