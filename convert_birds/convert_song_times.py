import re 
import datetime
import os


directory = os.path.dirname(os.path.abspath(__file__))

# Construct the path for the new directory
new_directory_path = os.path.join(directory, 'results')
# Create the new directory 
if os.path.isdir(new_directory_path) != True:
    os.mkdir(new_directory_path)


# Get a list of all files in the directory
file_list = os.listdir(directory)

# Iterate over each file
for file_name in file_list:
    # Create the absolute path of the file
    file_path = os.path.join(directory, file_name)
    
    # Check if the path is a file (not a directory)
    if os.path.isfile(file_path) and file_name.find('.txt') != -1 :
        sourceFile = open(file_path, "r")
        parsedFile  = open(f"results/converted_{file_name}", 'w'); 
        for line in sourceFile: 
            parsedData = line 
            # matchString = '(\d+-\d+)'
            if re.match( ".+(\d+(.\d)?-\d+(.\d)?).+", parsedData):
                seconds = re.search( '(\d+(.\d)?-\d+(.\d)?)', parsedData).group(0)   
                start, stop = seconds.split('-'); 
                tstart= str(datetime.timedelta(seconds=float(start)))
                tstop= str(datetime.timedelta(seconds=float(stop)))
                parsedData = parsedData.replace(seconds, f"{tstart}-{tstop}")
            elif bool(re.search( "\s(\d+(.\d)?)(\s|\n)", parsedData)):
                seconds = re.search( "\s(\d+(.\d)?)(\s|\n)", parsedData).group(1)   
                tstart= str(datetime.timedelta(seconds=float(seconds)))
                parsedData = parsedData.replace(seconds, f"{tstart}")


            parsedFile.write(parsedData)
        


