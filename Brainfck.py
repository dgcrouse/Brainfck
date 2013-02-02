# Add line to logfile
def logadd(col1,col2,col3,outfile):
    outfile.write('{:<4}{:<4}{:<4}\n'.format(col1,col2,col3))


import sys

# Initialize flags
debug = False   # Debug flag
verboseflag = False # Verbose output flag
verboseon = False   # Verbose output enabler
verbosefile = 0 # Logfile for verbose output

# Get code from argument
fileloc = str(sys.argv[1])
try:
	codefile = open(fileloc,'r')
except:
    print('Error reading code')
    sys.exit()
brainfck = codefile.read() # brainfck now holds code
codefile.close()


# Get command line options
optindx = 2 # Current index to read

# Loop over options
while optindx < len(sys.argv):
    option = sys.argv[optindx]
    
    # Set debug flag
    if option == '-debug':
        debug = True
        
    # Set verbose flag and prep logfile
    elif option == '-verbose':
        verboseflag = True
        verbosefile = open('log.txt','w')
        logadd('Cmd','Pos','Val',verbosefile)
        
    optindx+=1  # Increment option index
    
    

# Set up for code

# Initialize bytecache with 1 kB (will dynamically grow as needed)
myBytes = bytearray(1000)

# Initialize counters
currchar = 0    # Current pos in code
currbyte = 0    # Current pos in memory
currin = 0      # Current pos in input
maxbyte = 0     # Maximum number of bytes in memory used


# Prescan for brackets (initial optimization)
bracketstack = [] # Stack for searching brackets
inbrackets = [] # Stores indices of [
outbrackets=[] # Stores indices of ]
idx = 0 # index in code of current char

# Loop over code
for char in brainfck:
    # Push open bracket onto stack
    if char == '[':
        bracketstack.append(idx)
        # For close bracket, pop stack and add indices to lists
    if char == ']':
        try:
            inbrackets.append(bracketstack.pop())
        # Handle error
        except:
            print('Error! Unmatched ] exists')
            sys.exit()
        outbrackets.append(idx)
    idx+=1
    
# Handle error
if len(bracketstack) > 0:
    print('Error! Unmatched [ exists')
    sys.exit()

# Do we need input?
if brainfck.find(',') != -1:
        instr = str(raw_input('Enter Input: '))
    
# Read code char by char
while currchar < len(brainfck):
    
    # Assume character can be read
    usable = True
    
    
    if brainfck[currchar] == '>':
        currbyte+=1
        if currbyte > maxbyte:
            maxbyte = currbyte
        #If we run off the end, then we add another kB
        if currbyte == len(myBytes):
            myBytes += bytearray(1000)
            
        
    elif brainfck[currchar] == '<':
        currbyte-=1
        
    elif brainfck[currchar] == '+':
        # Wraparound
        if myBytes[currbyte] == 255:
            myBytes[currbyte] = 0
        else:
            myBytes[currbyte]+=1;
            
    elif brainfck[currchar] == '-':
        # Wraparound
        if myBytes[currbyte] == 0:
            myBytes[currbyte] = 255
        else:
            myBytes[currbyte]-=1;
            
    elif brainfck[currchar] == '.':
        sys.stdout.write(chr(myBytes[currbyte]))
        
    elif brainfck[currchar] == ',':
        if currin == len(instr):
            print('')
            sys.exit()
        myBytes[currbyte] = instr[currin]
        currin += 1
        
    elif brainfck[currchar] == '[' and myBytes[currbyte] == 0:
        currchar = outbrackets[inbrackets.index(currchar)]
                
    elif brainfck[currchar] == ']' and myBytes[currbyte] != 0:
        currchar = inbrackets[outbrackets.index(currchar)]
        
    # Debug symbol - Prints bytevalue
    elif brainfck[currchar] == '!' and debug:
        sys.stdout.write(str(myBytes[currbyte]))
        
    # Debug symbol - Dumps entirety of used memory
    elif brainfck[currchar] == '#' and debug:
        count = 0
        while count <= maxbyte:
            sys.stdout.write(str(myBytes[count]))
            sys.stdout.write(' ')
            count +=1
        sys.stdout.write('\n')
    
    # Beginning/end of verbose flags
    elif brainfck[currchar] == '$' and verboseflag:
        if verboseon:
            verboseon = False
        else:
            verboseon = True
            logadd('',str(currbyte),str(myBytes[currbyte]),verbosefile)
    
    else:
        # unusable character
        usable = False
        
    # Print command, current byte number, and current byte value
    if usable and verboseon:
        logadd(brainfck[currchar],str(currbyte),str(myBytes[currbyte]),verbosefile)
    
    currchar+=1 # move to next character
    
# Close logfile if opened
if verboseflag:
    verbosefile.close()