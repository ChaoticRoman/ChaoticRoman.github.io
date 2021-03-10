	#!/usr/bin/env python

import os
from eeschema import Sch, Component, TextItem, Wire, Sheet
from refTools import niceRefOffset
import numpy as np



def splitRef(ref):
    try:
        pos = map(str.isdigit, ref).index(True)
    except:
        print 'Probably not annotated reference "%s"'%ref
    return ref[:pos], int(ref[pos:])



def clone(template_fn, output_fn, posXY=(1000, 1000), clonesXY=(1, 1),
          margin=500, ref_offset=0, ref_spacing=0):
    
    template = Sch.load(template_fn)
    originalItems = template.items
    
    max_refnum = 0
    drawings, to_copy = [], []
    
    for item in template.items:
        if (type(item) == Wire) and (item.wireType1=='Notes'):
            drawings.append(item)
        else:
            if type(item) == Component:
                ref = item.ref
                max_refnum = max(max_refnum, splitRef(ref)[1])
            
    if ref_spacing:
        if ref_spacing<max_refnum:
            ValueError('ref_spacing %d smaller than max ref %d of target'
                        % (ref_spacing, max_refnum))
    else:
        ref_spacing = niceRefOffset(max_refnum)
    
    xs, ys = [], []
    for d in drawings:
        xs += [d.posA[0], d.posB[0]]
        ys += [d.posA[1], d.posB[1]]
        template.items.remove(d)    # do not copy borders
        
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    
    
    top_left = np.array([xmin, ymin])
    pos = np.array(posXY)
    vect0 = pos - top_left
    vectX = np.array( [xmax - xmin + margin, 0] )
    vectY = np.array( [0, ymax - ymin + margin] )
    
    new_items = []
    for item in template.items:
        item.Move(vect0)
        for j in range(clonesXY[1]):
            for i in range(clonesXY[0]):
                if i>0 or j>0:
                    newItem = item.Clone()
                    newItem.Move(i*vectX + j*vectY)
                        
                    if type(item) is Component:
                        splittedRef = splitRef( newItem.ref )
                        newRefNum = splittedRef[1] + (i+clonesXY[0]*j)*ref_spacing + ref_offset
                        newItem.ref = ''.join( [splittedRef[0], str(newRefNum)] )
                        
                    if type(item) is TextItem and item.labelType=='HLabel':
                        if clonesXY[0]*clonesXY[1]>1:
                            newItem.text = ("%s%d" % (item.text[:-1], i+clonesXY[0]*j,))
                        elif clonesXY[0]*clonesXY[1]==1:
                            newItem.text = ("%s" % (item.text,))
                        
                    new_items.append(newItem)
                else:
                    if type(item) is Component:
                        splittedRef = splitRef( item.ref )
                        newRefNum = splittedRef[1] + ref_offset
                        item.ref = ''.join( [splittedRef[0], str(newRefNum)] )
                        
                    if type(item) is TextItem and item.labelType=='HLabel':
                        if clonesXY[0]*clonesXY[1]>1:
                            item.text = ("%s%d" % (item.text, i+clonesXY[0]*j,))
                        elif clonesXY[0]*clonesXY[1]==1:
                            item.text = ("%s" % (item.text,))
        #template.items.remove(item)
                            
    template.items += new_items
    template.comments[0] = ("template='%s' N-clones=%d ref-offset=%d ref-spacing=%d"
                            % (os.path.abspath(template_fn),
                               clonesXY[0]*clonesXY[1], ref_offset, ref_spacing) )
    template.save(output_fn)
    
def buildSheet(input_fn):
    fname = os.path.split(input_fn)[-1]

    sheet = eeschema.Sheet()
    sheet.fileName = fname
    sheet.sheetName = fname.split('.')[0]
    sheet.pos[0]=3000
    sheet.pos[1]=1500
    
    sheet.dims[0]=1400
            
    sheet.pins = []
    pins = []
    
    try:
        subsheet = Sch.load(input_fn)
    except Exception as e:
        print 'Error "', e, '" when loading subsheet in file', str(input_fn)
        
    HLabels = subsheet.getTextItems('HLabel')
    pins = map(lambda label: label.text, HLabels)
    pins = sorted(set(pins))
    
    Npins = len(set([p[0] for p in pins]))
    
    print set([p[0] for p in pins])
    
    sheet.dims[1] = 400 + 100 * len(pins) + Npins*100
    
    target.items.append(sheet)
    posY = sheet.pos[1]+200
    last = 0
    for i, p in enumerate(pins):
        if int(p[0])>last:
            last += 1
            posY += 200
        else:
            posY += 100
            
        sheet.addPin(p, position=(sheet.pos[0], posY))
    
    target.save(sheetSchFN)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Klone template schematics to output schematics.')

    parser.add_argument('-i', '--input-sch', action="store", required=True, help='Template to inject.')
    parser.add_argument('-o', '--output-sch', action="store", required=True, help='Output schematics path and filename')
    parser.add_argument('-p', '--posXY', nargs=2, action="store", default=(1000, 1000), help='Position in target')
    parser.add_argument('-x', '--clonesX', action="store", default=1, help='Number of clones in X', type=int)
    parser.add_argument('-y', '--clonesY', action="store", default=1, help='Number of clones in Y', type=int)
    parser.add_argument('-m', '--margin', action="store", default=500, help='Margin between clones', type=int)
    parser.add_argument('-d', '--ref-offset', action="store", default=0, help='Between clones.', type=int)
    parser.add_argument('-r', '--ref-spacing', action="store", default=0, help='Between clones.', type=int)
    parser.add_argument('-s', '--out-sheet-sch', action="store", default=None, help='Hierarchical sheet output.')

    args = parser.parse_args()
    
    template_fn, output_fn = args.input_sch, args.output_sch
    pos, clonesX, clonesY = args.posXY, args.clonesX, args.clonesY
    margin = args.margin
    ref_spacing = args.ref_spacing
    ref_offset = args.ref_offset
    sheetSchFN = args.out_sheet_sch

    
    clone(template_fn, output_fn, posXY=(1000, 1000), clonesXY=(1, 1), margin=500, ref_offset=0, ref_spacing=0)
    print 'Saved to', output_fn


    if sheetSchFN:
        buildSheet(output_fn, sheetSchFN)
        print 'Saved to', sheetSchFN

        
