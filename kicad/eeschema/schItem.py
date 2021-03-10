
# TODO:
# 1. Hieararchic sheets, including their pins and recursive operation on them
# 3. Automatic application of applyToSource before rendering




import numpy as np


# opening tokens are always line begining
# EndSignal is either string (sheet, component or bitmap) or number of lines of the item
openingTokensToEndSignal = {
    '$Comp'          : '$EndComp',
    'NoConn ~ '      : 1,
    'Connection ~ '  : 1,
    'Text'           : 2,
    'Entry'          : 2,
    'Wire'           : 2,
    '$Sheet'         : '$EndSheet',
    '$Bitmap'        : '$EndBitmap'
}

openingTokens = openingTokensToEndSignal.keys()


def findAll(string, substring, overlapping=False):
    
    result = []
    pos = string.find(substring)
    
    if overlapping:
        L = 1
    else:
        L = len(substring)
    
    while pos>-1:
        result.append(pos)
        pos = string.find(substring, pos+L)
        
    return result

def getFromSource(src, row, col):
    if col>-1:
        
        # following is for items in apostrofes to be taken as one item even with spaces
        line = src.split('\n')[row]
        apostrofes = findAll(line, '"')
        splittedLine = []
        pos = 0
        for i in range( len(apostrofes)//2 ):
            opening, closing = apostrofes[2*i], apostrofes[2*i+1]
            if opening > pos:
                splittedLine += line[pos:opening].split()
            splittedLine += [line[opening+1:closing],]
            pos = closing+1
        if pos<len(line):
            splittedLine += line[pos:].split()
        return splittedLine[col]
    
    elif col==-1:
        return src.split('\n')[row]
    else:
        ValueError('Invalid col %s' % str(col))    

def getFirstApostrofesFromLine(src, row):
    line = src.split('\n')[row]
    pos1 = line.find('"')+1
    pos2 = line.find('"', pos1)
    return line[pos1:pos2]


def setInSource(src, row, col, val):
    lines = src.split('\n')
    if col>-1:
        line = lines[row].strip()
        apostrofes = findAll(line, '"')
        splittedLine = []
        pos = 0
        for i in range( len(apostrofes)//2 ):
            opening, closing = apostrofes[2*i], apostrofes[2*i+1]
            if opening > pos:
                splittedLine += line[pos:opening].split()
            splittedLine += [line[opening:closing+1] ,]
            pos = closing+1
        
        if pos<len(line):
            splittedLine += line[pos:].split()
        val = str(val)
        
        if val=='' or ( ( (' ' in val) or (splittedLine[col][0]=='"' and splittedLine[col][-1]=='"') ) and (val[0]!='"' or val[-1]!='"') ):
            splittedLine[col] = '"' + str(val) + '"'
        else:
            splittedLine[col] = str(val)
        line = ' '.join(splittedLine)
        lines[row] = line
    elif col==-1:
        lines[row] = str(val)
    else:
        ValueError('Invalid col %s' % str(col))    
    
    return '\n'.join(lines)

def setFirstApostrofesInLine(src, row, value):
    lines = src.split('\n')
    line = lines[row]
    pos1 = line.find('"')+1
    pos2 = line.rfind('"')
    newLine = line[:pos1] + str(value) + line[pos2:]
    lines[row] = newLine
    return '\n'.join(lines)




        
class SchItem(object):
    
    def __init__(self, source=None):
        if source:
            self.source = source
        else:
            self.source = self.default_source
        
        self.build(self.source)
        
    def __repr__(self):
        return self.source

    def __str__(self):
        return str(type(self))

    #def build(self, source): # Uncomment for dummys function enable
        #pass
    
    def Move(self, vect):
        self.pos += vect
        self.applyToSource()
        
    def Clone(self):
        return (type(self))(source=self.source)

    
class Component(SchItem):
    #openning_token = '$Comp'
    default_source = """$Comp
L LED D1
U 1 1 54CE0528
P 5650 3350
F 0 "D1" H 5650 3450 50  0000 C CNN
F 1 "LED" H 5650 3250 50  0000 C CNN
F 2 "SMD_Packages:SMD-0805" H 5650 3150 60  0000 C CNN
F 3 "" H 5650 3350 60  0000 C CNN
\t1    5650 3350
\t0    -1   1    0   
$EndComp"""

    def build(self, source):
        self.ref = getFromSource(source, 1, 2)
        self.value = getFromSource(source, 5, 2)
        self.footprint = getFromSource(source, 6, 2)
        self.unit = int(getFromSource(source, 2, 1))
        self.fontSize = int(getFromSource(source, 4, 6))
        self.pos = np.array(map(int, [getFromSource(source, 3, 1), getFromSource(source, 3, 2)]))
        
        
    def applyToSource(self):
        src = str(self.source)
        
        src = setInSource(src, 1, 2, self.ref)
        src = setInSource(src, 4, 2, '"%s"' % (self.ref, ))
        
        src = setInSource(src, 2, 1, "%d" % (self.unit, ))
        
        src = setInSource(src, 4, 6, "%d" % (self.fontSize, ))
        src = setInSource(src, 5, 6, "%d" % (self.fontSize, ))
        src = setInSource(src, 6, 6, "%d" % (self.fontSize, ))
        
        
        old_pos = np.array(map(int, [getFromSource(src, 3, 1), getFromSource(src, 3, 2)]))
        src = setInSource(src, 3, 1, "%d" % (self.pos[0], ))
        src = setInSource(src, 3, 2, "%d" % (self.pos[1], ))
        #print src
        src = src.replace('\t1   ','^!TAB$^')
        src = setInSource(src, 8, 1, "%d" % (self.pos[0], ))
        src = setInSource(src, 8, 2, "%d" % (self.pos[1], ))
        #print src
        
        src = src.replace('^!TAB$^','\t1   ')
        
        for i in range(4, 8):
            #print i, src.split('\n')[i]
            old_label_pos = np.array(map(int, [getFromSource(src, i, 4), getFromSource(src, i, 5)]))
            diff = old_label_pos - old_pos
            new_label_pos = self.pos + diff
            src = setInSource(src, i, 4, "%d" % (new_label_pos[0], ))
            src = setInSource(src, i, 5, "%d" % (new_label_pos[1], ))
        
        
        self.source = src
        
    def __str__(self):
        #return str(type(self)) + ' ref. ' + self.ref + '(unit '+ str(self.unit) +') at ' + str(self.pos) 
        return  'Item of type %s, ref. %s (unit %d) at %s' % (str(type(self)), self.ref, self.unit, str(self.pos))



class TextItem(SchItem):
    #openning_token = 'Text'
    default_source = """Text HLabel 5650 3150 0    60   Input ~ 0
Hiearchical label"""

    def build(self, source):
        self.labelType = getFromSource(source, 0, 1)
        self.pos = np.array(map(int, [getFromSource(source, 0, 2), getFromSource(source, 0, 3)]))
        self.fontSize = int(getFromSource(source, 0, 5))
        self.text = getFromSource(source, 1, -1)
        
        
    def applyToSource(self):
        src = str(self.source)
        
        src = setInSource(src, 0, 1, self.labelType)
        src = setInSource(src, 0, 2, "%d" % (self.pos[0], ))
        src = setInSource(src, 0, 3, "%d" % (self.pos[1], ))
        src = setInSource(src, 0, 5, "%d" % (self.fontSize, ))
        src = setInSource(src, 1, -1, self.text)
        
        self.source = src
        
        
    def __str__(self):
        #return str(type(self)) + ' ref. ' + self.ref + '(unit '+ str(self.unit) +') at ' + str(self.pos) 
        return  'Item of type %s, type %s, text %s at %s' % (str(type(self)), self.labelType, self.text, str(self.pos))



class Entry(SchItem):
    #openning_token = 'Entry'
    default_source = """Entry Wire Bus
4100 2300 4200 2400"""

    def build(self, source):
        self.entryType1 = getFromSource(source, 0, 1)
        self.entryType2 = getFromSource(source, 0, 2)
        self.posA = np.array(map(int, [getFromSource(source, 1, 0), getFromSource(source, 1, 1)]))
        self.posB = np.array(map(int, [getFromSource(source, 1, 2), getFromSource(source, 1, 3)]))
        
        
    def applyToSource(self):
        src = str(self.source)
        
        src = setInSource(src, 0, 1, self.entryType1)
        src = setInSource(src, 0, 2, self.entryType2)
        src = setInSource(src, 1, 0, "%d" % (self.posA[0], ))
        src = setInSource(src, 1, 1, "%d" % (self.posA[1], ))
        src = setInSource(src, 1, 2, "%d" % (self.posB[0], ))
        src = setInSource(src, 1, 3, "%d" % (self.posB[1], ))        
        
        self.source = src
        
        
    def __str__(self):
        #return str(type(self)) + ' ref. ' + self.ref + '(unit '+ str(self.unit) +') at ' + str(self.pos) 
        #return  'Item of type %s, type %s, text %s at %s' % (str(type(self)), self.labelType, self.text, str(self.pos)
        return  'Item of type %s %s %s from %s to %s' % (str(type(self)), self.entryType1, self.entryType2, (self.posA), str(self.posB))

    def Move(self, vect):
        self.posA += vect
        self.posB += vect
        self.applyToSource()

        
class Wire(SchItem):
    #openning_token = 'Wire'
    default_source = """Wire Wire Line
        5600 3550 5650 3550"""

    def build(self, source):
        self.wireType1 = getFromSource(source, 0, 1)
        self.wireType2 = getFromSource(source, 0, 2)
        self.posA = np.array(map(int, [getFromSource(source, 1, 0), getFromSource(source, 1, 1)]))
        self.posB = np.array(map(int, [getFromSource(source, 1, 2), getFromSource(source, 1, 3)]))
        
        
    def applyToSource(self):
        src = str(self.source)
        
        src = setInSource(src, 0, 1, self.wireType1)
        src = setInSource(src, 0, 2, self.wireType2)
        src = setInSource(src, 1, 1, "%d" % (self.posA[1], ))
        src = setInSource(src, 1, 2, "%d" % (self.posB[0], ))
        src = setInSource(src, 1, 3, "%d" % (self.posB[1], ))
        src = setInSource(src, 1, 0, "\t%d" % (self.posA[0], )) # is first because of tabulator on the beginning
        
        self.source = src
           
    def __str__(self):
        #return str(type(self)) + ' ref. ' + self.ref + '(unit '+ str(self.unit) +') at ' + str(self.pos) 
        return  'Item of type %s %s %s from %s to %s' % (str(type(self)), self.wireType1, self.wireType2, str(self.posA), str(self.posB))
    
    def Move(self, vect):
        self.posA += vect
        self.posB += vect
        self.applyToSource()


        
class Sheet(SchItem):   # FIXME: pin subclass
    #openning_token = '$Sheet'
    default_source = '''$Sheet
S 1800 1600 1500 1500
F0 "test" 60
F1 "test.sch" 60
F2 "CLK" O R 3300 1800 60 
F3 "/RESET" O R 3300 2000 60 
F4 "VPWR" O R 3300 2700 60 
F5 "/HALT" O R 3300 2100 60 
F6 "TRANSF1" I L 1800 1900 60 
F7 "TRANSF2" I L 1800 2000 60 
F8 "3.84MH" O R 3300 2200 60 
$EndSheet'''

    def build(self, source):
        #print source
        splittedSource = source.split('\n')
        if splittedSource[2][0] == 'U': # time stamp present, remove it
            source = '\n'.join(splittedSource[:2] + splittedSource[3:])
            self.source = source
        #print source
        self.pos = np.array(map(int, [getFromSource(source, 1, 1), getFromSource(source, 1, 2)]))
        self.dims = np.array(map(int, [getFromSource(source, 1, 3), getFromSource(source, 1, 4)]))
        self.sheetName =  getFirstApostrofesFromLine(source, 2)
        self.fileName =  getFirstApostrofesFromLine(source, 3)
        
        #print source
        lines = source.split('\n')[4:-1]
        pinCount = len(lines)
        lines = '\n'.join(lines)
        
        #print lines
        self.pins = [ [getFirstApostrofesFromLine(lines, i), getFromSource(lines, i, 2),\
                       getFromSource(lines, i, 3), np.array(map(int, [getFromSource(lines, i, 4), \
                       getFromSource(lines, i, 5)]))] for i in range(pinCount) ]
                   #FIXME can have spaces, correctly by "" and spaces
                   
    
    def addPin(self, pinName, inputoutput='I', leftright='L', position=None, offset=100):
        if not position:
            if leftright=='L':
                x = self.pos[0]
            else:
                x = self.pos[0] + self.dims[0]
                
            y = offset + max([self.pos[1], ] + [p[3][1] for p in self.pins if p[2]==leftright])
            
            position = np.array([x, y])
            
        pin = [pinName, inputoutput, leftright, position]
        self.pins.append(pin)
        
        
    def applyToSource(self):
        src = str(self.source)
        
        src = setInSource(src, 1, 1, "%d" % (self.pos[0], ))
        src = setInSource(src, 1, 2, "%d" % (self.pos[1], ))
        src = setInSource(src, 1, 3, "%d" % (self.dims[0], ))
        src = setInSource(src, 1, 4, "%d" % (self.dims[1], ))

        src = setFirstApostrofesInLine(src, 2, self.sheetName)
        src = setFirstApostrofesInLine(src, 3, self.fileName)
        
        pin = self.pins
        
        pinLines = ['F%d "%s" %s %s %d %d 60' % (i+2, pin[i][0], pin[i][1], pin[i][2], \
                                                 pin[i][3][0], pin[i][3][1]) for i in range(len(pin))]
        srcLines = src.split('\n')
        
        self.source = '\n'.join(srcLines[:4] + pinLines + srcLines[-1:])
    
    def __str__(self):
        #return str(type(self)) + ' ref. ' + self.ref + '(unit '+ str(self.unit) +') at ' + str(self.pos) 
        header =  'Item of type %s at %s of dims %s, %s/%s' % (str(type(self)), str(self.pos), \
                                                             str(self.dims), self.fileName, self.sheetName) 
        return header + '\n' + '\n'.join(map(str, self.pins))
        
        # FIXME can have spaces, correctly by ""

def Bitmap(SchItem):
    pass




class NoConnect(SchItem):
    openning_token = 'NoConn ~ '
    default_source = """NoConn ~ 1000 1000"""

    def build(self, source):
        self.pos = np.array(map(int, [getFromSource(source, 0, 2), getFromSource(source, 0, 3)]))
        
        
    def applyToSource(self):
        src = str(self.source)
        
        src = setInSource(src, 0, 2, "%d" % (self.pos[0], ))
        src = setInSource(src, 0, 3, "%d" % (self.pos[1], ))
        
        self.source = src
           
    def __str__(self):
        #return str(type(self)) + ' ref. ' + self.ref + '(unit '+ str(self.unit) +') at ' + str(self.pos) 
        return  'Item of type %s at %s' % (str(type(self)), str(self.pos))



class Connection(SchItem):
    openning_token = 'Connection ~ '
    default_source = """Connection ~ 1000 2000"""

    def build(self, source):
        self.pos = np.array(map(int, [getFromSource(source, 0, 2), getFromSource(source, 0, 3)]))
        
        
    def applyToSource(self):
        src = str(self.source)
        
        src = setInSource(src, 0, 2, "%d" % (self.pos[0], ))
        src = setInSource(src, 0, 3, "%d" % (self.pos[1], ))
        
        self.source = src
           
    def __str__(self):
        #return str(type(self)) + ' ref. ' + self.ref + '(unit '+ str(self.unit) +') at ' + str(self.pos) 
        return  'Item of type %s at %s' % (str(type(self)), str(self.pos))


        
        
        
        
        
        
        
        
        

# opening tokens are always on line begining
openingTokensToClasses = {
    '$Comp'          : Component,
    'NoConn ~ '      : NoConnect,
    'Text'           : TextItem,
    'Wire'           : Wire,
    'Connection ~ '  : Connection,
    'Entry'          : Entry,
    '$Sheet'         : Sheet,
    '$Bitmap'        : Bitmap
}



def parseItems(source_lines):
    items = []
    
    L = len(source_lines)
    line = 0
    
    while line < L:
        
        found = False
        for token in openingTokens:
            token_len = len(token)
            if source_lines[line][:token_len] == token:
                endSignal = openingTokensToEndSignal[token]
                if type(endSignal) == int:
                    ItemSrc = source_lines[line:line + endSignal]
                    line += endSignal-1
                elif type(endSignal) == str:
                    #print source_lines[line+1:]
                    endRelativePos = source_lines[line+1:].index(endSignal)
                    ItemSrc = source_lines[line:line + 2 + endRelativePos]
                    line += endRelativePos+1
                    
                    
                new_item = openingTokensToClasses[token]('\n'.join(ItemSrc))
                items.append(new_item)
                found = True
                break
            
        if not found:
            raise ValueError('Unknown token')
    
        line += 1
        
    
    
    
    return items
    
    
if __name__ == '__main__':
    #print Component.openning_token
    test = """$Comp
L R R1
U 1 1 54CE04A8
P 5350 3550
F 0 "R1" V 5430 3550 50  0000 C CNN
F 1 "R" V 5357 3551 50  0000 C CNN
F 2 "SMD_Packages:SMD-0805" V 5550 3550 30  0000 C CNN
F 3 "" H 5350 3550 30  0000 C CNN
        1    5350 3550
        0    1    1    0   
$EndComp
$Comp
L LED D1
U 1 1 54CE0528
P 5650 3350
F 0 "D1" H 5650 3450 50  0000 C CNN
F 1 "LED" H 5650 3250 50  0000 C CNN
F 2 "SMD_Packages:SMD-0805" H 5650 3150 60  0000 C CNN
F 3 "" H 5650 3350 60  0000 C CNN
        1    5650 3350
        0    -1   1    0   
$EndComp
Wire Wire Line
        5600 3550 5650 3550
Text HLabel 5650 3150 0    60   Input ~ 0
LED_A_$(#)
$Comp
L GND #PWR01
U 1 1 54CE070A
P 5100 3550
F 0 "#PWR01" H 5100 3300 60  0001 C CNN
F 1 "GND" H 5100 3400 60  0000 C CNN
F 2 "" H 5100 3550 60  0000 C CNN
F 3 "" H 5100 3550 60  0000 C CNN
        1    5100 3550
        1    0    0    -1  
$EndComp"""

    items = parseItems(test.splitlines())
    
    for i in items:
        print type(i)
        print i
        print