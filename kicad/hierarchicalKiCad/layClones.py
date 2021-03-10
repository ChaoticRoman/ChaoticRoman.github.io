#!/usr/bin/python2.7
import os
import wx
import string, itertools

import eeschema, pcbnew

# Base pcbnew functions
from pcbnew import LoadBoard

# Nice datatypes
from pcbnew import wxPoint, MODULE, TRACK, TEXTE_PCB, DIMENSION
from pcbnew import DRAWSEGMENT, ZONE_CONTAINER, VIA

# PCB Layers
from pcbnew import Edge_Cuts

# Utility functions
from pcbnew import FromMils, FromMM, ToMils, ToMM
from pcbnew import GetKicadConfigPath




mm = 1e6       # mm/nm, note: nm is internal pcbnew unit (IU)
A4 = 297*mm, 210*mm  # nm
px_per_nm = 2e-6  # pixels per mm
W, H = A4[0]*px_per_nm, A4[1]*px_per_nm # pixels

PAD = 15*mm



def getBounds(pcb):
        outPoints = []
        for Draw in pcb.GetDrawings():
                if type(Draw) is DRAWSEGMENT and(Draw.GetShapeStr()=='Line')\
                        and(Draw.GetLayer()==Edge_Cuts):
                                #Draw.SetWidth(FromMils(10))
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
                        lsItems.append(Item)
                        
        nZones = pcb.GetAreaCount()
        if nZones:
                for idx in range(nZones):
                        Zone = pcb.GetArea(idx)
                        if type(Zone)==nullType:
                                raise TypeError, "Null Object Error#%i, expected Zone/Area Type" % (idx+1,)
                        lsItems.append(Zone)
                        
        return lsItems


def processRef(ref, copy, ref_spacing, ref_offset):
    
    i = -1
    digits = string.digits
    
    if not ref[-1] in digits: raise ValueError('strange reference "%s"'%ref)
    while ref[i-1] in digits:
        i -= 1
        
    basename, num = ref[:i], int(ref[i:])
    
    return basename + '%d' % (num + ref_offset + copy*ref_spacing,)





class clonesLayoutApp(wx.Frame):

    def __init__(self, parent, id, mainSchPath=None, boardSize=None, title='Hierarchical KiCad'):
        
        wx.Frame.__init__(self, parent, id, title, size=(1000, 800))
        panel = wx.Panel(self)
        
        ### LAYOUT
        #######################################################################
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        WIDGETS_PADDING = 2
        
        hbox.Add(vbox1, 1, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        hbox.Add(vbox2, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        
        panel.SetSizer(hbox)
            

        ### FIRST COLUMN: SETTING
        #######################################################################
        # First line: tree of sublayouts
        font = wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTSTYLE_NORMAL)
        layoutTree = wx.TreeCtrl(panel,
                                 style=wx.TR_FULL_ROW_HIGHLIGHT|wx.TR_MULTIPLE)
        layoutRoot = layoutTree.AddRoot('Board')
        layoutTree.SetItemFont(layoutRoot, font)
        #layoutTree.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.modifyItem)
        #layoutTree.Bind(wx.EVT_LIST_ITEM_SELECTED, self.modifyItemIfSelected)
        
        vbox1.Add(layoutTree, 1, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        layoutTree.ExpandAll()
        
        # Second line: controls
        hbox13 = wx.BoxSizer(wx.HORIZONTAL)
        VCenterBut = wx.Button(panel, label='Vertical center')
        HCenterBut = wx.Button(panel, label='Horizontal center')
        
        VCenterBut.Bind(wx.EVT_BUTTON, self.VCenter)
        HCenterBut.Bind(wx.EVT_BUTTON, self.HCenter)
        
        hbox14 = wx.BoxSizer(wx.HORIZONTAL)
        LEdgeBut = wx.Button(panel, label='Left edge')
        REdgeBut = wx.Button(panel, label='Right edge')
        TEdgeBut = wx.Button(panel, label='Top edge')
        BEdgeBut = wx.Button(panel, label='Bottom edge')
        
        LEdgeBut.Bind(wx.EVT_BUTTON, self.LEdge)
        REdgeBut.Bind(wx.EVT_BUTTON, self.REdge)
        TEdgeBut.Bind(wx.EVT_BUTTON, self.TEdge)
        BEdgeBut.Bind(wx.EVT_BUTTON, self.BEdge)
        
        hbox15 = wx.BoxSizer(wx.HORIZONTAL)
        #RotBut   = wx.Button(panel, label='Rotate clockwise')
        #FlipBut  = wx.Button(panel, label='Flip')
        LBut   = wx.Button(panel, label='Left')
        RBut   = wx.Button(panel, label='Right')
        UBut   = wx.Button(panel, label='Up')
        DBut   = wx.Button(panel, label='Down')
        
        
        LAlignBut  = wx.Button(panel, label='Align left')
        RAlignBut  = wx.Button(panel, label='Align right')
        UAlignBut  = wx.Button(panel, label='Align up')
        DAlignBut  = wx.Button(panel, label='Align down')
        
        LBut.Bind(wx.EVT_BUTTON, self.Left)
        RBut.Bind(wx.EVT_BUTTON, self.Right)
        UBut.Bind(wx.EVT_BUTTON, self.Up)
        DBut.Bind(wx.EVT_BUTTON, self.Down)
        
        LAlignBut.Bind(wx.EVT_BUTTON, self.LAlign)
        RAlignBut.Bind(wx.EVT_BUTTON, self.RAlign)
        UAlignBut.Bind(wx.EVT_BUTTON, self.UAlign)
        DAlignBut.Bind(wx.EVT_BUTTON, self.DAlign)
        
        hbox16 = wx.BoxSizer(wx.HORIZONTAL)
        saveBut = wx.Button(panel, label='Save')
        
        saveBut.Bind(wx.EVT_BUTTON, self.save)
        
        hbox13.Add(HCenterBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox13.Add(VCenterBut, 1, wx.ALL, WIDGETS_PADDING)
        
        hbox14.Add(LEdgeBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox14.Add(REdgeBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox14.Add(TEdgeBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox14.Add(BEdgeBut, 1, wx.ALL, WIDGETS_PADDING)
        
        #hbox15.Add(RotBut, 1, wx.ALL, WIDGETS_PADDING)
        #hbox15.Add(FlipBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox15.Add(LBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox15.Add(RBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox15.Add(UBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox15.Add(DBut, 1, wx.ALL, WIDGETS_PADDING)
        
        hbox16.Add(LAlignBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox16.Add(RAlignBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox16.Add(UAlignBut, 1, wx.ALL, WIDGETS_PADDING)
        hbox16.Add(DAlignBut, 1, wx.ALL, WIDGETS_PADDING)
        
        
        vbox1.Add(hbox13, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        vbox1.Add(hbox14, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        vbox1.Add(hbox15, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        vbox1.Add(hbox16, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        vbox1.Add(saveBut, 0, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        
        
        ### SECOND COLUMN: SCHEMATICS PREVIEW AND LOG
        #######################################################################
        pcbPanel = wx.Panel(panel, size=(W+1, H+1))
        pcbPanel.SetBackgroundColour('white')
        pcbPanel.Bind(wx.EVT_PAINT, self.OnPaint)
        
        logText = wx.TextCtrl(panel, value='', style=wx.TE_MULTILINE)
        
        vbox2.Add(pcbPanel, 0, wx.ALL, WIDGETS_PADDING)
        vbox2.Add(logText, 1, wx.ALL|wx.EXPAND, WIDGETS_PADDING)
        
       
        ### PUBLIC WIDGETS
        ########################################################################
        self.logText = logText
        self.layoutTree, self.layoutRoot = layoutTree, layoutRoot
        self.pcbPanel = pcbPanel
        self.font = font
        
        ### PUBLIC DATA
        ########################################################################
        self.title = title
        self.mainSchPath = mainSchPath
        self.superitems = dict()  # wx.TreeItemId to dictionary
        self.items = dict()       # wx.TreeItemId to dictionary
        self.boardSize = boardSize
        self.boardPos = boardSize
        
        ### CENTRE AND SHOW 
        ########################################################################
        self.Centre()
        self.Show(True)
        self.log('Program started.')
        self.load()
        self.OnPaint(None)


    def load(self):
        mainSchPath = self.mainSchPath
        superitems = self.superitems
        layoutTree, layoutRoot = self.layoutTree, self.layoutRoot

        if not mainSchPath:
            dlg = wx.FileDialog(self, "Choose a schematics.", './', "", "*.sch", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                directory, mainSchFileName = dlg.GetDirectory(), dlg.GetFilename()
                mainSchPath = os.path.join(directory, mainSchFileName)
            dlg.Destroy()
        else:
            directory, mainSchFileName = os.path.split(mainSchPath)
        
        if not self.boardSize:
            ok = False
            while not ok:
                dlg = wx.TextEntryDialog(self,
                    'Board size WxH, where W and H is width and heigth in mm, i.e. "100x50".',
                    caption=self.title, defaultValue='')
                
                if dlg.ShowModal() == wx.ID_OK: ## TODO Do something when invalid input recieved
                    try:
                        vals = dlg.GetValue().split('x')
                        boardSize = list(map(int, vals))
                        ok = True
                    except:
                        pass
                dlg.Destroy()
        else:
            boardSize = map(int, self.boardSize)
        
        layoutTree.SetItemText(layoutRoot, 'Board "%s" of size %dmm x %dmm' % (mainSchFileName[:-4], boardSize[0], boardSize[1]))
        #self.log('Board of size %s at %s' % (str(boardSize), str(self.boardPos)))
        
        boardSize = [boardSize[0]*mm, boardSize[1]*mm]
        self.boardSize = boardSize
        self.boardPos = (A4[0]-boardSize[0])/2, (A4[1]-boardSize[1])/2
        
        
        mainSch = eeschema.Sch.load(self.mainSchPath)

        freepos = [PAD, PAD]
        max_height_in_line = 0
        for sheet in mainSch.getSheets():
            # Load schematics, copies, ref_offset and ref_spacing from subschematics
            #######################################################################
            name, fileName = sheet.sheetName, sheet.fileName
            path = os.path.join(directory, fileName)
            subsch = eeschema.Sch.load(path)
            
            metadata = str(subsch.comments[0])[10:]
            index = metadata.index("'")
            template = metadata[:index]

            metadata = metadata[index+2:]
            metadata = metadata[9:]
            index = metadata.index(" ")
            copies = int(metadata[:index])

            metadata = metadata[13:]
            index = metadata.index(" ")
            ref_offset = int(metadata[:index])

            metadata = metadata[index+13:]
            ref_spacing = int(metadata[:])
            self.log( '%s +%d %dx%d' % (template, ref_offset, copies, ref_spacing) )
            
            # Get cloned template board size and position
            ###############################################
            
            inputPCB = LoadBoard(template[:-4] + '.kicad_pcb')
            (x_min, y_min), (x_max, y_max) = getBounds(inputPCB)
            inputPCBTopLeft = wxPoint(x_min, y_min)
            inputPCBBottomRight = wxPoint(x_max, y_max)
            inputPCBDimensions = inputPCBBottomRight - inputPCBTopLeft
            
            # Build tree items
            #####################
            # 1. Superitems
            
            itemLabel = '%s%s%7.3f x%7.3f' % (name, max(1,16-len(name))*' ', inputPCBDimensions[0]/1e6, inputPCBDimensions[1]/1e6)
            
            newSuperItem = layoutTree.AppendItem(layoutRoot, itemLabel)
            layoutTree.SetItemFont(newSuperItem, self.font)
            superitems[newSuperItem] = dict()
            superitems[newSuperItem]['name'] = name
            superitems[newSuperItem]['template'] = template
            superitems[newSuperItem]['copies'] = copies
            superitems[newSuperItem]['ref_offset']  = ref_offset
            superitems[newSuperItem]['ref_spacing'] = ref_spacing
            superitems[newSuperItem]['original_pos'] = inputPCBTopLeft
            superitems[newSuperItem]['size'] = inputPCBDimensions
            superitems[newSuperItem]['inputPCB'] = inputPCB

            superitems[newSuperItem]['childs'] = []
            # 2. Single clones
            for i in range(copies):
                child = dict()
                if freepos[0] + inputPCBDimensions[0] > A4[0]:
                    freepos[0] = PAD
                    freepos[1] += max_height_in_line + PAD
                    max_height_in_line = 0
                else:
                    max_height_in_line = max(max_height_in_line, inputPCBDimensions[1])
                    
                pos = list(freepos)
                freepos[0] += inputPCBDimensions[0] + PAD
                    
                newItem = layoutTree.AppendItem(newSuperItem, '')
                layoutTree.SetItemFont(newItem, self.font)
                child['clone_num'] = i
                child['wx_parent'] = newSuperItem
                child['wx_handler'] = newItem
                child['pos'] = pos
                child['rot'] = 0
                child['flipped'] = ' '
                
                superitems[newSuperItem]['childs'].append(child)
                self.items[newItem] = child
                
            
            
    def rebuildCloneLabels(self):
        layoutTree = self.layoutTree
        boardPos = self.boardPos
        items = self.items
        
        for wx in items:
            item = items[wx]
            i, pos, rot, flip = item['clone_num'], item['pos'], item['rot'], item['flipped']
            
            itemText = '#%d %s %7.3f,%7.3f; %5.1f%s' % (i, (10-len('%d'%i))*' ',
                                                        (pos[0]-boardPos[0])/mm, (pos[1]-boardPos[1])/mm,
                                                        rot, flip)
            layoutTree.SetItemText(wx, itemText)
        
        layoutTree.ExpandAll()
    
    def getSelected(self):
        layoutTree = self.layoutTree
        selection = layoutTree.GetSelections()
        items, superitems = self.items, self.superitems
        selected_superitems, selected_items = [], []
        
        for handler in selection:
            if handler in items.keys():
                selected_items.append(handler)
            elif handler in superitems.keys():
                selected_superitems.append(handler)
        
        root = (layoutTree.GetRootItem() in selection)
        return len(selection), root, selected_superitems, selected_items
    
    
    def getItemByWxHandler(self, handler): # WTF?! "in keys" query says it is in but direct access per key says KeyError
                                           # This hack works...
        return [self.items[k] for k in self.items.keys() if handler in [k,]][0]
    
    #def getSuperitemByWxHandler(self, handler): # WTF?! #2 This is not needed and self.superitems[item['wx_parent']] is good enough!!!
        #return [self.superitems[k] for k in self.superitems.keys() if handler in [k,]][0]
    
    
    def HCenter(self, event):
        self._Center(0)
    
    def VCenter(self, event):
        self._Center(1)
    
    def _Center(self, coord):
        log = self.log
        N_selected, root_selected, selected_superitems, selected_items = self.getSelected()
        if N_selected and N_selected == len(selected_items):
            sizes, poses = [], []
            for _id in selected_items:
                item = self.getItemByWxHandler(_id)
                sizes.append(self.superitems[item['wx_parent']]['size'][coord])
                poses.append(item['pos'][coord])
            mini = min(poses)
            maxi = max([poses[i]+sizes[i] for i in range(len(poses))])
            vec = (A4[coord] - maxi - mini)/2
            
            for _id in selected_items:
                item = self.getItemByWxHandler(_id)
                size = self.superitems[item['wx_parent']]['size']
                item['pos'][coord] += vec
            self.OnPaint(None)
        else:
            log('Implemented for clones only')
    
    def LEdge(self, event):
        self._Edge(0, -1)
    
    def REdge(self, event):
        self._Edge(0, 1)
    
    def TEdge(self, event):
        self._Edge(1, -1)
    
    def BEdge(self, event):
        self._Edge(1, 1)
        
    def _Edge(self, coord, bottomright):
        log = self.log
        N_selected, root_selected, selected_superitems, selected_items = self.getSelected()
        if N_selected == len(selected_items):
            for _id in selected_items:
                item = self.getItemByWxHandler(_id)
                size = self.superitems[item['wx_parent']]['size']
                item['pos'][coord] = (A4[coord] + bottomright*self.boardSize[coord])/2 - (1+bottomright)/2*size[coord]
            self.OnPaint(None)
        else:
            log('Implemented for clones only')
    
    
    def Left(self, event):
        self._Move(0, -1)
    
    def Right(self, event):
        self._Move(0,  1)
    
    def Up(self, event):
        self._Move(1, -1)
    
    def Down(self, event):
        self._Move(1,  1)
        
    def _Move(self, coord, sign):
        log = self.log
        N_selected, root_selected, selected_superitems, selected_items = self.getSelected()
        if N_selected == len(selected_items):
            for _id in selected_items:
                item = self.getItemByWxHandler(_id)
                item['pos'][coord] += sign*5*mm
            self.OnPaint(None)
        else:
            log('Implemented for clones only')
    
    
    def LAlign(self, event):
        self._Align(0, -1)
    
    def RAlign(self, event):
        self._Align(0, 1)
    
    def UAlign(self, event):
        self._Align(1, -1)
    
    def DAlign(self, event):
        self._Align(1, 1)
        
    def _Align(self, coord, sign):
        log = self.log
        N_selected, root_selected, selected_superitems, selected_items = self.getSelected()
        
        if N_selected == len(selected_items) and N_selected>1:
            
            first = self.getItemByWxHandler(selected_items[0])
            last_pos = first['pos'][coord]
            for _id in selected_items[1:]:
                item = self.getItemByWxHandler(_id)
                rev = [1, 0][coord]
                item['pos'][rev] = first['pos'][rev]
                last_pos = last_pos + sign * self.superitems[item['wx_parent']]['size'][coord]
                item['pos'][coord] = last_pos 
            self.OnPaint(None)
            
        else:
            log('Implemented for N>1 clones only')
    
    
    def OnPaint(self, event):
        
        self.rebuildCloneLabels()
        
        boardPos, boardSize = self.boardPos, self.boardSize
        
        dc = wx.PaintDC(self.pcbPanel)
        dc.Clear()
        superitems = self.superitems

        dc.SetPen(wx.Pen('black'))
        dc.SetFont(self.font)
        
        #dc.DrawRectangle(0,0,W,H) # draw inside :(
        def rec(x,y,w,h):
            x,y,w,h = map(int, (x,y,w,h))
            dc.DrawLine(x,y,x+w,y)
            dc.DrawLine(x+w,y,x+w,y+h)
            dc.DrawLine(x+w,y+h,x,y+h)
            dc.DrawLine(x,y+h,x,y)
        
        rec(0,0,W,H)
        if boardPos:
            rec(boardPos[0]*px_per_nm,  boardPos[1]*px_per_nm,
                boardSize[0]*px_per_nm, boardSize[1]*px_per_nm)
            
        for _id in superitems:
            superitem = superitems[_id]
            #print superitem['name']
            for i, item in enumerate(superitem['childs']):
                pos, size = item['pos'], superitem['size']
                rec(pos[0]*px_per_nm, pos[1]*px_per_nm, size[0]*px_per_nm, size[1]*px_per_nm)
                name = '%d' %i
                extent = dc.GetFullTextExtent(name)
                dc.DrawRotatedText(name,
                    (pos[0] + size[0]/2)*px_per_nm - extent[0]/2,
                    (pos[1] + size[1]/2)*px_per_nm - extent[1]/2, 0)

           
        
    def log(self, msg):
        l = self.logText
        l.SetValue(l.GetValue() + str(msg) + '\n')

    def save(self, event):
        
        mainSchPath = self.mainSchPath
        superitems = self.superitems
        
        targetPCBPath = mainSchPath[:-4] + '.kicad_pcb'
        targetPCB = LoadBoard(targetPCBPath)
        
        targetPCBTopLeft = wxPoint(*self.boardPos)
        targetPCBSize    = wxPoint(*self.boardSize)
        targetPCBSizeX   = wxPoint(self.boardSize[0], 0)
        targetPCBSizeY   = wxPoint(0 ,self.boardSize[1])
        
        ### Plot board outline to target board
        ##########################################
        # Crazy code, modified from pcbnew_easy...
        layer_dict = {pcbnew.BOARD_GetStandardLayerName(n):n for n in range(pcbnew.LAYER_ID_COUNT)}
        get_layer = lambda s: layer_dict.get(s)
        def add_line(start, end, layer='Edge.Cuts', width=0.15*mm):
            """Create a graphic line on the board"""
            a = DRAWSEGMENT(targetPCB)
            a.SetShape(pcbnew.S_SEGMENT)
            a.SetStart(start)
            a.SetEnd(end)
            a.SetLayer(get_layer(layer))
            a.SetWidth(int(width))
            targetPCB.Add(a)
            return a

        add_line(targetPCBTopLeft, targetPCBTopLeft + targetPCBSizeX)
        add_line(targetPCBTopLeft + targetPCBSizeX, targetPCBTopLeft + targetPCBSize)
        add_line(targetPCBTopLeft + targetPCBSize, targetPCBTopLeft + targetPCBSizeY)
        add_line(targetPCBTopLeft + targetPCBSizeY, targetPCBTopLeft)
        
        
        ### Move and orient imported modules and plot tracks, vias and zones
        ########################################################################
        # Create dict of reference to module in target board
        targetModules = dict()
        for i in brdItemize(targetPCB):
            if type(i) == MODULE:
                targetModules[i.GetReference()]=i
        
        # For every subcircuit layout
        for _id in superitems:
            superitem = superitems[_id]
            template = superitem['template']
            #self.log('')
            #self.log(template)
            inputPCB = LoadBoard(template[:-4] + '.kicad_pcb')
            
            # get info about sublayout
            inputPCBTopLeft = wxPoint(*superitem['original_pos'])

            types = set()
            for item in brdItemize(inputPCB):
                itemType = type(item)
                types.add(itemType)
                for i in range(superitem['copies']):
                    pos = wxPoint(*superitem['childs'][i]['pos'])
                    #self.log(str((i, pos)))
                    if itemType == MODULE:
                        
                        ref = item.GetReference()
                        new_ref = processRef(ref, i, superitem['ref_spacing'], superitem['ref_offset'])
                        
                        if item.IsFlipped() and not targetModules[new_ref].IsFlipped():
                            targetModules[new_ref].Flip(targetModules[new_ref].GetPosition())
                            
                        targetModules[new_ref].SetOrientation(item.GetOrientation())  # TODO real orientation
                                                
                        vect = pos - targetModules[new_ref].GetPosition() + item.GetPosition() - inputPCBTopLeft
                        targetModules[new_ref].Move(vect)
                        
                    elif itemType == TRACK:
                        t = TRACK(targetPCB)
                        t.SetWidth(item.GetWidth())
                        t.SetLayer(item.GetLayer())
                        t.SetStart(item.GetStart() - inputPCBTopLeft +  pos)
                        t.SetEnd(item.GetEnd() - inputPCBTopLeft +  pos)
                        targetPCB.Add(t)
                        
                    elif itemType == VIA:
                        v = VIA(targetPCB)
                        v.SetViaType(item.GetViaType())
                        v.SetWidth(item.GetWidth())
                        v.SetPosition(item.GetPosition() - inputPCBTopLeft +  pos)
                        targetPCB.Add(v)
                        
                    #elif itemType == ZONE_CONTAINER:
                        #z = ZONE_CONTAINER(targetPCB)
                        #for i in range(item.GetNumCorners()):
                            #z.AppendCorner(item.GetCornerPosition(i))
                        #z.SetPosition(item.GetPosition() + pos - inputPCBTopLeft)
                        #z.SetHatchStyle(item.GetHatchStyle())
                        #z.SetFillMode(item.GetFillMode())
                        #z.SetMinThickness(item.GetMinThickness())
                        #z.AddFilledPolysList(item.GetFilledPolysList())
                        #z.SetOutline(item.Outline())
                        #targetPCB.Add(z)
                        
                        
            for t in types:
                self.log(t)

        directory, targetPCBFileName = os.path.split(targetPCBPath)
        
        outPath = os.path.join(directory, targetPCBFileName)
        targetPCB.Save(outPath)
        self.log('Saved to %s.' % outPath)
    
        
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='KiCad PCB cloning tool.')
    
    parser.add_argument('sch', nargs='?', action="store", default=None, help='High-level schematics generated with HierarchicalKiCad.')
    parser.add_argument('-b', nargs=2, action="store", default=None, help='Board size in mm.')
    args = parser.parse_args()

    mainSchPath = args.sch
    boardSize = args.b
    
    app = wx.App()
    clonesLayoutApp(None, -1, mainSchPath, boardSize=boardSize)
    app.MainLoop()
