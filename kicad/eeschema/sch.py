# Strings
import schItem

header = 'EESchema Schematic File Version 2'
footer = '$EndSCHEMATC\n'
A3_landscape = 'A3 16535 11700'
A4_landscape = 'A4 11693 8268'

class Sch(object):
    def __init__(self, source=None):
        self.libraries = []
        self.sheet_format = A4_landscape
        self.encoding = 'utf-8'
        self.current_sheet = 1
        self.total_sheets = 1
        self.title = ''
        self.date = ''
        self.rev = ''
        self.comp = ''
        self.comments = ['', '', '', '']
        
        self.items = []
        
        self.cwd = './'
        
        
        if type(source)==Sch:
            src = repr(source)
        elif not source:
            src = None
            self.libraries = ['power', 'device']
        else:
            src = source
            
        if type(src)==str:
            lines = src.splitlines()
            if lines[0][:len(header)] != header:
                raise ValueError('Bad header', lines[0])
            
            if '\n'.join(lines[-1:]) != footer[:-1]:
                raise ValueError('Bad footer', '\n'.join(lines[-2:]))
            
            line=1
            
            while lines[line][:5] == 'LIBS:':
                self.libraries += [lines[line][5:], ]
                line += 1
                
            while lines[line][:8] == 'EELAYER ':
                line += 1
                
            if lines[line][:7] == '$Descr ':
                self.sheet_format = lines[line][7:]
                line += 1
            else:
                raise ValueError('Bad line "' + lines[line] + '". "$Descr ..." expected' )
                
                
            if lines[line][:9] == 'encoding ':
                self.encoding = lines[line][9:]
                line += 1
            else:
                self.encoding = None    ### Seems be optional
                
            if lines[line][:6] == 'Sheet ':
                self.current_sheet, self.total_sheets = map(int, lines[line][6:].split(' '))
                line += 1
            else:
                raise ValueError('Bad line ' + lines[line])
            
            if lines[line][:7] == 'Title "':
                self.title = lines[line][7:-1]
                line += 1
            else:
                raise ValueError('Bad line ' + lines[line])
            
            if lines[line][:6] == 'Date "':
                self.date = lines[line][6:-1]
                line += 1
            else:
                raise ValueError('Bad line ' + lines[line])
            
            if lines[line][:5] == 'Rev "':
                self.rev = lines[line][5:-1]
                line += 1
            else:
                raise ValueError('Bad line ' + lines[line])
            
            if lines[line][:6] == 'Comp "':
                self.comp = lines[line][6:-1]
                line += 1
            else:
                raise ValueError('Bad line ' + lines[line])
            
            
            for i in range(4):
                if lines[line][:10] == 'Comment%d "'%(i+1):
                    self.comments[i] = lines[line][10:-1]
                    line += 1
                else:
                    raise ValueError('Bad line ' + lines[line])
                            
            if lines[line] != '$EndDescr':
                raise ValueError('Bad line ' + lines[line])
            else:
                line += 1
                
            self.items = schItem.parseItems(lines[line:-1])
                        
    
        
    def __repr__(self):
        
        source = header + '\n'
        
        for lib in self.libraries:
            source += 'LIBS:%s\n' % lib
            
        source += 'EELAYER 25 0\nEELAYER END\n$Descr %s\n' % self.sheet_format
        if self.encoding:
            source += 'encoding %s\n' % (self.encoding)
        source += 'Sheet %d %d\n' % (self.current_sheet, self.total_sheets)
        source += 'Title "%s"\n' % (self.title)
        source += 'Date "%s"\n' % (self.date)
        source += 'Rev "%s"\n' % (self.rev)
        source += 'Comp "%s"\n' % (self.comp)
        for i in range(4):
            source += 'Comment%d "%s"\n' % (i+1, self.comments[i])
        source += '$EndDescr\n'
        
        for item in self.items:
            item.applyToSource()
            source += repr(item) + '\n'
        
        source += footer
        
        return source
     
     
    def __str__(self):
        message = 'KiCad schematics "' + self.title + '", date "' + self.date
        message += '", rev "' + self.rev + '", sheet format "' + self.sheet_format + '"'
        return message
    
    @classmethod
    def load(self, fn):
        f = open(fn, 'r')
        src = f.read()
        f.close()
        sch = Sch(src)
        sch.cwd = '/'.join(fn.split('/')[:-1]) + '/'
        return sch
    
    def save(self, fn):
        f = open(fn, 'w')
        #print repr(self)
        f.write(repr(self))
        f.close()
        
    def getComponents(self):
        return [item for item in self.items if type(item) is schItem.Component]
    
    def getWires(self):  # All line items
        return [item for item in self.items if type(item) is schItem.Wire]
    
    def getSheets(self):  # All sheet items
        return [item for item in self.items if type(item) is schItem.Sheet]
    
    def getTextItems(self, textItemType=None):  # All line items
        txts = [item for item in self.items if type(item) is schItem.TextItem]
        if textItemType:
            txts = [item for item in txts if item.labelType==textItemType]
        return txts
    
    
    def insertSubsheet(self, name, fn, position=(1000, 1000), size=(1600, None)):
        sheet = schItem.Sheet()
        sheet.pos[0]=position[0]
        sheet.pos[1]=position[1]
        sheet.dims[0]=size[0]
        if size[1]:
            sheet.dims[1]=size[1]
        
        sheet.sheetName, sheet.fileName = name, fn.split('/')[-1]
        sheet.pins = []
        pins = []
        
        try:
            subsheet = Sch.load(self.cwd+fn)
            HLabels = subsheet.getTextItems('HLabel')
            pins = map(lambda label: label.text, HLabels)
            pins = sorted(set(pins))
            #print pins
            
        except Exception as e:
            print 'Error "', e, '"for subsheet in file', str(self.cwd+fn)
        
        
        if not size[1]:
            sheet.dims[1] = 200 + 100 * len(pins)
        for p in pins:
            sheet.addPin(p)
        
        self.items.append(sheet)
        
    def getSubitems(self):
        
        result = list(self.items)
        for item in self.getSheets():
            try:
                subsheet = Sch.load(self.cwd+item.fileName)
                result  += subsheet.getSubitems()
            except Exception as e:
                print e, 'for subsheet', str(item)
            
        return result
        
        

if __name__=='__main__':    
    
    from schItem import Component, NoConnect, TextItem, Wire, Sheet
    import numpy as np
    
    
    ### TEST 0 EMPTY SCHEMATICS
    #sch = Sch()
    #print sch   # The same as print str(sch)
    #print 50*'-'
    #print repr(sch)
    
    
    
    ### TEST 1 CREATE SCHEMATICS
    #sch.items = [Component(), NoConnect(), TextItem(), Wire()]
    
    #sch.save('./test0.sch')
    
    #sch.items[0].ref = 'D2'
    #sch.items[0].pos += np.array([500, 0])
    #sch.items[0].applyToSource()
    
    #print sch
    #print
    #print repr(sch)
    #print
    ##print sch.items
    #print
    #for i in sch.items:
        #print i
        #print repr(i)
        #print
    
    
    #### TEST 2 READ AND MODIFY SCHEMATICS

    #f = open('./test.sch', 'r')
    #src = f.read()
    #f.close()
    
    #sch = Sch(src)

    #output_src = repr(sch)
    ##print output_src
    
    #vector_move = np.array([-1000, 0])
    
    #i=1
    #for item in sch.items:
        
        #item.pos += vector_move
        #if type(item) == Component:
            #item.ref = 'D%d'%i
            #i +=1
            #item.applyToSource()
        #if type(item) == TextItem:
            #item.text = 'Ahoj'
            #item.applyToSource()
                    
    #for i in sch.items:
        #print i
        
    #raw_input()


    ### TEST 3: MULTIPLE CLONES SCHEMATICS

    sch = Sch.load('../hierarchicalKiCad/testFiles/to_multiply.sch')

    #output_src = repr(sch)
    #print output_src
    
    vector_x = np.array([1500, 0])
    vector_y = np.array([0, 1500])
    
    N, M = 2, 4
    i, j = 1, 1
    newItems = []
    hLabels = []
    
    for item in sch.items:
        for i in range(N):
            for j in range(M):
                
                newItem = item.Clone()
                
                if type(item) == Component:
                    new_ref = item.ref[0] + str(i*M + j)
                    newItem.ref = new_ref
                    
                elif type(item) == TextItem:
                    newItem.text = item.text.replace('$(#)', str(i*M + j))
                    if newItem.labelType == 'HLabel':
                        hLabels.append(newItem.text)
                    
                    
                newItem.Move(vector_y*i + vector_x*j)
                
                newItems.append(newItem)
            
                
        
        #item.applyToSource()
        
    for i in sch.items:
        print i
    #raw_input()
    
    
    sch.items = newItems
    
    
    for i in sch.items:
        print i
    #raw_input()
    
    outfn = './test.sch'
    sch.save(outfn)
    print '%s saved.' % outfn
    
    
    sch = Sch()
    sheet = Sheet()
    sch.items = [sheet,]
    
    
    
    sheet.pins = []
    for label in hLabels:
        if '4' in label:
            sheet.addPin(label, offset=200)
        else:
            sheet.addPin(label)
    sheet.applyToSource()
    
    
    for i in sch.items:
        print i
    outfn = './testSheet.sch'
    sch.save(outfn)
    print '%s saved.' % outfn
    
    
    
    
    
    
    
    
    ### DIFF
    
    #original_src_lines = src.splitlines()
    #new_src_lines = output_src.splitlines()
    
    #L0, L1 = len(original_src_lines), len(new_src_lines)
    
    #if L0>L1:
        #print 'OOPS! Missing ' + str(L0-L1) + ' lines!'
    #elif L0<L1:
        #print 'OOPS! There is ' + str(L1-L0) + ' new lines!'
    
    #print 'diff... ',
    #for i in range(min(L0, L1)):
        #orig, new = original_src_lines[i], new_src_lines[i]
        #if orig != new:
            #print 'orig:', orig
            #print 'new:', new
            #print
            
    #print 'done.'
    