import copy
from wave20261105_arm7_boundary_next_flow import analyze


def execute(image,base,entries,flow,nativeHash):
    from wave20261105_arm7_boundary_next_audit import certificate,protected_intersections,NAMESPACE
    begin=int(flow['entry'],0);end=int(flow['computedEvidenceEndExclusive'],0);rejected=[]
    for label in ['wrong-mode','invented-Thumb-fragment','wrong-native-hash','neighbor-envelope-extension','missing-suffix-read','wrong-literal-origin','wrong-literal-width','wrong-instruction-word','unclassified-byte-count']:
        altered=copy.deepcopy(flow);raw=image;expected=nativeHash
        if label=='wrong-mode':altered['entryMode']='thumb'
        elif label=='invented-Thumb-fragment':altered['instructions'][0]['mode']='thumb'
        elif label=='wrong-native-hash':expected='0'*64
        elif label=='neighbor-envelope-extension':altered['computedEvidenceEndExclusive']=hex(end+4);altered['computedEvidenceEnvelopeBytes']+=4
        elif label=='missing-suffix-read':altered['literalReads']=[r for r in altered['literalReads'] if int(r['address'],0)!=end-4]
        elif label=='wrong-literal-origin':altered['literalReads'][0]['origin']=hex(begin)
        elif label=='wrong-literal-width':altered['literalReads'][0]['bytes']=2
        elif label=='wrong-instruction-word':altered['instructions'][0]['word']='0'
        else:altered['literalReadBytes']+=4
        try:certificate(altered,raw,base,expected)
        except ValueError as error:rejected.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid physical certificate accepted: '+label)
    structural=[]
    for label,address,word in [('lost-upper-bound-condition',0x027e0920,0xaa00000c),('lost-unsigned16-source',0x027e0908,0xe599200c),('table-branch-is-call',0x027e0930,0xeb000016),('unproved-dynamic-PC-target',0x027e0928,0xe1a0f000),('ARMv5-only-CLZ',begin,0xe16f0f10)]:
        changed=bytearray(image);changed[address-base:address-base+4]=word.to_bytes(4,'little');result=analyze(bytes(changed),base,begin)
        if result['completePhysicalEvidence']:raise ValueError('Unsupported/incomplete analysis-only control admitted: '+label)
        structural.append(dict(case=label,analysisOnlyInMemoryTamper=True,sourceCredit=0,unresolved=result['unresolved'],unaccountedRanges=result['unaccountedRanges'],rejected=True))
    bare=analyze(image,base,begin)
    withEntries=analyze(image,base,begin,entries)
    if any(bare[k]!=withEntries[k] for k in ['computedEvidenceEndExclusive','reachableInstructionBytes','literalReadBytes','instructionRanges','literalReadRanges']) or not bare['completePhysicalEvidence']:raise ValueError('Extent depends on neighboring entry inventory')
    protection=[]
    for label,namespace,first,last,blocked in [('ARM7-function-interior',list(NAMESPACE),begin+4,begin+8,True),('mode-independent-Thumb-alias',list(NAMESPACE),begin+4,begin+8,True),('suffix-data-storage',list(NAMESPACE),end-4,end+4,True),('next-adjacent-function',list(NAMESPACE),end,end+4,False),('ARM9-numeric-collision',['','arm9','arm7-main'],begin,end,False),('child-program-numeric-collision',['dwc/utility.bin/move/child.srl','arm7','arm7-main'],begin,end,False)]:
        record=dict(namespace=namespace,start=first,end=last,kind='controlled-protection',mode='thumb' if 'Thumb' in label else 'arm');actual=bool(protected_intersections(begin,end,[record]))
        if actual!=blocked:raise ValueError('Physical namespace/storage/mode protection control differs: '+label)
        protection.append(dict(case=label,expectedBlocked=blocked,actualBlocked=actual,passed=True))
    return dict(status='passed',sourceCredit=0,nativeOrSourceExecuted=0,certificateNegativeControls=rejected,structuralAnalysisNegativeControls=structural,protectionControls=protection,nextEntryIndependence=dict(passed=True,entryInventoryProvidedForPrimaryAnalysis=False,inventoryRemovedRetainsSameExtent=True,bytes=bare['computedEvidenceEnvelopeBytes']),limits=['Modified words exist only in analysis-control byte arrays; no native image/object/source/registry/config or accepted bytes are patched. No control grants source ownership/credit.'])
