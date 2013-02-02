import sys, clipboard, console

brainfck = clipboard.get()

# Set up for code

# Initialize bytecache with 1 kB (will dynamically grow as needed)
myBytes = bytearray(1000)

# Initialize counters
currchar = 0
currbyte = 0
currin = 0

# Prescan for brackets (initial optimization)
bracketstack = [] # Stack for searching brackets
inbrackets = [] # Stores indices of [
outbrackets=[] # Stores indices of ]
idx = 0 # index in code of current char

for char in brainfck:
    # Push open bracket onto stack
    if char == '[':
        bracketstack.append(idx)
        # For close bracket, pop stack and add indices to lists
    if char == ']':
        try:
            inbrackets.append(bracketstack.pop())
        except:
            print('Error! Unmatched ] exists')
            sys.exit()
        outbrackets.append(idx)
    idx+=1
if len(bracketstack) > 0:
    print('Error! Unmatched [ exists')
    sys.exit()


# Do we need input?
if brainfck.find(',') != -1:
        instr = console.input_alert('Enter Input', 'Enter Input')
    
# Read code char by char
while currchar < len(brainfck):
    if brainfck[currchar] == '>':
        currbyte+=1
        
        # If we run off the end, then we add another kB
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
        
    currchar+=1