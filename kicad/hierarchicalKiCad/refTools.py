from eeschema import Component


def splitRef(ref):  #not annotated item: D? -> None
    pos = map(str.isdigit, ref)
    if True in pos:
        pos = pos.index(True)
        return ref[:pos], int(ref[pos:])
    else:
        return ref, None
    
    

def maxRefNumber(target):
    taget_refs = []
    max_refnum = 0
    #for i in target.getSubitems(): print i
    for item in target.getSubitems():
        if type(item) is Component:
            ref = item.ref
            taget_refs.append(ref)
            max_refnum = max(max_refnum, splitRef(ref)[1])
            
    return max_refnum
    

def niceRefOffset(max_refnum):
    margin_ref = 2*max_refnum
    if margin_ref<1:
        ref_offset_per_injection = 0
    elif margin_ref<10:
        ref_offset_per_injection = 10
    elif margin_ref<20:
        ref_offset_per_injection = 20
    elif margin_ref<50:
        ref_offset_per_injection = 50
    elif margin_ref<100:
        ref_offset_per_injection = 100
    elif margin_ref<200:
        ref_offset_per_injection = 200
    elif margin_ref<500:
        ref_offset_per_injection = 500
    elif margin_ref<1000:
        ref_offset_per_injection = 1000
    elif margin_ref<2000:
        ref_offset_per_injection = 2000
    elif margin_ref<5000:
        ref_offset_per_injection = 5000
    elif margin_ref<10000:
        ref_offset_per_injection = 10000
    else:
        ValueError('To high ref_offset %d found.' % max_refnum)

    return ref_offset_per_injection



