#!/bin/bash/python2.7

# Base pcbnew functions
from pcbnew import LoadBoard

# Nice datatypes
from pcbnew import wxPoint, MODULE, TRACK, TEXTE_PCB, DIMENSION
from pcbnew import DRAWSEGMENT

# PCB Layers
from pcbnew import Edge_Cuts

# Utility functions
from pcbnew import FromMils, FromMM, ToMils, ToMM
from pcbnew import GetKicadConfigPath

import string


fileNamePCB = './testFiles/single_channel_backannotated.kicad_pcb'
fileNameSave = './testFiles/test1.kicad_pcb'

ref_offset = 100


               

def brdBounds(pcb):
        outPoints = []
        for Draw in pcb.GetDrawings():
                if type(Draw) is DRAWSEGMENT and(Draw.GetShapeStr()=='Line')\
                        and(Draw.GetLayer()==Edge_Cuts):
                                Draw.SetWidth(FromMils(10))
                                for pnt in (Draw.GetStart(), Draw.GetEnd()):
                                        if pnt not in outPoints:
                                                outPoints.append(pnt)
                                                
        x_min, y_min = x_max, y_max = outPoints[0]
        for x, y in outPoints:
                x_min = min(x_min, x)
                y_min = min(y_min, y)
                x_max = max(x_max, x)
                y_max = max(y_max, y)
                
        return (x_min, y_min), (x_max, y_max)


def brdItemize(pcb):
        lsItems = []
        nullType = type(None)
        for ItemStr in ('Drawings', 'Tracks', 'Modules'):
                for idx, Item in enumerate(getattr(pcb, 'Get'+ItemStr)()):
                        if type(Item)==nullType:
                                raise TypeError, "Null Object Error#%i, expected %s Type" % (idx+1, ItemStr[:-1])
                        Item.remove = False
                        lsItems.append(Item)
        nZones = pcb.GetAreaCount()
        if nZones:
                for idx in range(nZones):
                        Zone = pcb.GetArea(idx)
                        if type(Zone)==nullType:
                                raise TypeError, "Null Object Error#%i, expected Zone/Area Type" % (idx+1,)
                        Zone.remove = False
                        lsItems.append(Zone)
        return lsItems

def brdDrawInEdge(Item, orginBounds):
        if type(Item) is not DRAWSEGMENT:
                return False
        if Item.GetLayer()!=Edge_Cuts:
                return False
        (xa, ya), (xb, yb) = orginBounds
        if Item.GetShapeStr()=='Line':
                x1, y1 = Item.GetStart()
                x2, y2 = Item.GetEnd()
                if x1==x2 and(x1 in (xa, xb)):
                        return True
                if y1==y2 and(y1 in (ya, yb)):
                        return True
        # Other Shapes in Future
        return False



def brdRotate(wxCenter, angle):
        for Item in lsItems:
                Item.Rotate(wxCenter, angle)

def brdPosite(ptFrom, ptTo):
        vect = wxPoint(ptTo[0]-ptFrom[0], ptTo[1]-ptFrom[1])
        for Item in lsItems:
                Item.Move(vect)




pcb = LoadBoard(fileNamePCB)

#print 'MODULES:'
#for Module in pcb.GetModules():
    #m = Module
    #print m
    
#bd = brdBounds(pcb)
lsItems = brdItemize(pcb)
#wxCenter = wxPoint((bd[0][0]+bd[1][0])/2, (bd[0][1]+bd[1][1])/2)


#vect = wxPoint(x*(vx+spaceX), y*(vy+spaceY))
mm=1e6
vect = wxPoint(0, -5*mm)

print 'ALL_ITEMS:'

processText = lambda originalText, copy: originalText.replace('$(#)', str('%d'%copy))

def processRef(ref, copy, offset):
    
    i = -1
    digits = string.digits
    
    if not ref[-1] in digits: raise ValueError('strange reference "%s"'%ref)
    while ref[i-1] in digits:
        i -= 1
        
    basename, num = ref[:i], int(ref[i:])
    
    return basename + '%d' % (copy*offset + num)

for Item in lsItems:
        if Item.remove:
                continue
        #elif brdDrawInEdge(Item, bd) or (type(Item) is DIMENSION):
                #Item.remove = True
                #continue # do not clone dimmensions or edge lines, a last one will be exchanged with generated grid
                
        itemType = type(Item)
        newItem = Item.Duplicate()
        print itemType
        if itemType == TEXTE_PCB:
            txt = Item.GetText()
            Item.SetText(processText(txt, 1))
            newItem.SetText(processText(txt, 2))
            
        elif itemType == MODULE:
            ref = Item.GetReference()
            Item.SetReference(processRef(ref, 1, ref_offset))
            newItem.SetReference(processRef(ref, 2, ref_offset))
        
        
        print newItem
        print type(newItem)
        print dir(newItem)
        #raw_input()
        
        
        pcb.Add(newItem)
        newItem.Move(vect)
        
        
pcb.Save(fileNameSave)