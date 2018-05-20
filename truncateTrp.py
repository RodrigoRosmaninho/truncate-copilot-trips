#coding=utf-8

#  _                              _    _______ _____  _____  
# | |                            | |  |__   __|  __ \|  __ \ 
# | |_ _ __ _   _ _ __   ___ __ _| |_ ___| |  | |__) | |__) |
# | __| '__| | | | '_ \ / __/ _` | __/ _ \ |  |  _  /|  ___/ 
# | |_| |  | |_| | | | | (_| (_| | ||  __/ |  | | \ \| |     
#  \__|_|   \__,_|_| |_|\___\__,_|\__\___|_|  |_|  \_\_|                                                          


# Python tool that 'truncates' CoPilot™ GPS trip files (.trp). Essentialy making a smaller, self-contained trip out of a larger one.
# No breach of any copyright was intended.

# Made by Rodrigo Rosmaninho (2018)
# Github Repository: https://github.com/RodrigoRosmaninho/truncate-copilot-trips

import traceback, argparse, sys, os.path, subprocess

# 'argparser' manages arguments and the 'help' message in the command line
global parser
# Instantiate the parser
parser = argparse.ArgumentParser(description='Python tool that \'truncates\' CoPilot trip files (.trp). Essentialy making a smaller, self-contained trip out of a larger one.')

# Specifies input file
parser.add_argument('-in', dest='fileIN',
                    help='Specifies the name of your input .trp file. The file you want to read from.')

# Specifies output file
parser.add_argument('-out', dest='fileOUT',
                    help='Specifies the name of your output .trp file. The file you want to write to.')

# Specifies start stop number
parser.add_argument('-start', dest='startStop',
                    help='Specifies the number of the stop you want to start at. This is optional.')

# Specifies end stop number
parser.add_argument('-end', dest='endStop',
                    help='Specifies the number of the stop you want to end at. This is optional.')

data = []

def main():
    global fileIN, fileOUT, start, end, args, data

    # Get arguments
    args = parser.parse_args()

    # If the value wasn't given as an argument, ask the user for it
    if args.fileIN == None:
        fileIN = input("Input .trp file: ")
    else:
        fileIN = args.fileIN

    # If the value wasn't given as an argument, ask the user for it
    if args.fileOUT == None:
        fileOUT = input("Output .trp file: ")
    else:
        fileOUT = args.fileOUT

    validate_file(fileIN)
    # CoPilot .trp files are encoded in UTF-8. Therefore, a temporary copy of the input file is created and converted to UTF-8 so that it can be read by this script without using '.decode()' 
    run_bash_command("iconv -f UTF-16 -t UTF-8 " + fileIN + " -o temp.trp")
    fileIN = open("temp.trp","r")
    # A temporary output file, encoded in UTF-8, is created. Later, it'll be converted to UTF-16
    tempOUT = open("temp2.trp", "w")
    fileOUT = open(fileOUT, "w")
    
    read_file(fileIN)

    # If the value wasn't given as an argument, ask the user for it
    if args.startStop == None:
        start = int(input("Choose start point: "))
    else:
        start = args.startStop

    # If the value wasn't given as an argument, ask the user for it
    if args.endStop == None:
        end = int(input("Choose end point: "))
    else:
        end = args.endStop

    write_file(start, end, tempOUT, fileOUT.name)
    tempOUT.close()
    # Generate the final output file, encoded in UTF-16, as a copy of the temporary output file
    run_bash_command("iconv -f UTF-8 -t UTF-16 temp2.trp -o " + fileOUT.name)
    # Delete both temporary files
    run_bash_command("rm temp.trp temp2.trp")

def validate_file(fname):
    if not os.path.exists(fname):
        sys.exit("Error! " + fname + " does not exist!")
    if os.path.isdir(fname):
        sys.exit("Error! " + fname + " is a directory!")
    if not os.path.isfile(fname):
        sys.exit("Error! " + fname + " is not a file!")

def run_bash_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

# Reads the file line by line saving the data for each stop in an object of class 'Stop'. All stops are saved in 'data', a list of 'Stop' objects
def read_file(file):
    global data
    current = -1
    stop = Stop()
    data=[]
    
    for line in file:
        if "Start Stop=Stop" in line:
            current += 1
            stop = Stop()
            stop.sequence = current
        elif "Name=" in line:
            stop.name = line[5:]
        elif "Address=" in line:
            stop.address = line[8:]
        elif "City=" in line:
            stop.city = line[5:]
        elif "State=" in line:
            stop.state = line[6:]
        elif "Country=" in line:
            stop.country = line[8:]
        elif "Longitude=" in line:
            stop.lng = line[10:]
        elif "Latitude=" in line:
            stop.lat = line[9:]
        elif "Show=" in line:
            stop.show = line[5:]
        elif ("End Stop" in line) and ("Opt" not in line):
            print("Stop " + str(stop.sequence), end="")
            if hasattr(stop, "name"):
                print(" -> " + stop.name, end="")
            else:
                print()
            data.append(stop)

# Accesses the list of stops, 'data', and writes only the stops in between the 'start' and 'end' values to a new file
def write_file(start, end, file, name):
    file.write("Data Version:2.14.6.1\n")
    file.write("Start Trip=" + name[:5] + "\n")
    file.write("Creator=Made with the truncateTrp tool by RodrigoRosmaninho\n")
    file.write("Memo=\n")
    file.write("End Trip\n\n")

    global data
    x = 0
    for i in range(int(start), int(end) + 1):
        file.write("Start Stop=Stop " + str(x) + "\n")
        if hasattr(data[i], "name"):
            file.write("Name=" + data[i].name)
        if hasattr(data[i], "address"):    
            file.write("Address=" + data[i].address)
        if hasattr(data[i], "city"):
            file.write("City=" + data[i].city)
        if hasattr(data[i], "state"):
            file.write("State=" + data[i].state)
        if hasattr(data[i], "country"):
            file.write("Country=" + data[i].country)
        if hasattr(data[i], "lng"):
            file.write("Longitude=" + data[i].lng)
        if hasattr(data[i], "lat"):
            file.write("Latitude=" + data[i].lat)
        if hasattr(data[i], "show"):
            file.write("Show=" + data[i].show)
        file.write("Sequence=" + str(x) + "\n")
        file.write("End Stop\n")
        file.write("\n")
        file.write("Start StopOpt=Stop " + str(x) + "\n")
        file.write("Loaded=1\n")
        file.write("End StopOpt\n")
        file.write("\n")
        x += 1


class Stop:
    global name, address, city, state, country, lng, lat, show, sequence
        

if __name__ == "__main__":
	main()