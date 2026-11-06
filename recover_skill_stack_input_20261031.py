import re
import qualified_skill_input_contexts_20261031 as Q
TYPE_NAME='NativeSavedSkillInput2_20261031'


def calls(source):
    pattern=r'\b(?:func_02062e44|native_fn_02062e44)\s*\('
    for match in re.finditer(pattern,source):
        start=match.end()
        depth=1
        pieces=[]
        prior=start
        for pos in range(start,len(source)):
            ch=source[pos]
            if ch=='(':depth+=1
            elif ch==')':
                depth-=1
                if depth==0:
                    pieces.append((prior,pos,source[prior:pos]))
                    break
            elif ch==',' and depth==1:
                pieces.append((prior,pos,source[prior:pos]))
                prior=pos+1
        else:raise ValueError('UnbalancedSkillInputCall')
        if len(pieces)==3:yield pieces[2]


def native_byte_stores(assembly):
    offsets=set()
    for line in assembly.splitlines():
        match=re.search(r'^\s*strb(?:eq|ne|cs|cc|mi|pl|vs|vc|hi|ls|ge|lt|gt|le)?\s+\w+,\s*\[sp(?:,\s*#(0x[0-9a-fA-F]+|[0-9]+))?\]',line)
        if match:offsets.add(int(match[1],0) if match[1] else 0)
    return offsets


def recover(source,assembly,module='main',processor='arm9',program=None):
    Q.apply('',module,processor=processor,program=program)
    candidates={}
    for start,end,text in calls(source):
        match=re.fullmatch(r'\s*(?:\(\s*(?:const\s+)?'+TYPE_NAME+r'\s*\*\s*\)\s*)?&\s*(sp[0-9a-fA-F]+)\s*',text)
        if match:candidates.setdefault(match[1],[]).append((start,end))
    if not candidates:return source,[]
    declarations={}
    for match in re.finditer(r'^([ \t]*)(s8|u8|signed char|unsigned char)\s+(sp[0-9a-fA-F]+);\s*$',source,re.M):
        name=match[3]
        offset=int(name[2:],16)
        if offset in declarations:raise ValueError('AmbiguousSkillStackOffset')
        declarations[offset]=(name,match)
    stores=native_byte_stores(assembly)
    changes=[]
    replacements=[]
    claimed=set()
    for base,spans in candidates.items():
        offset=int(base[2:],16)
        if claimed&{offset,offset+1}:raise ValueError('SkillInputOverlappingObjectClaims')
        claimed.update((offset,offset+1))
        if offset not in declarations or offset+1 not in declarations:raise ValueError('SkillInputAdjacentByteMissing')
        first,decl0=declarations[offset]
        second,decl1=declarations[offset+1]
        if first!=base:raise ValueError('SkillInputBaseOffsetAmbiguous')
        if not {offset,offset+1}<=stores:raise ValueError('SkillInputNativeByteStoresMissing')
        for name,decl in ((first,decl0),(second,decl1)):
            for use in re.finditer(r'\b'+re.escape(name)+r'\b',source):
                if decl.start()<=use.start()<decl.end():continue
                if name==first and any(a<=use.start()<b for a,b in spans):continue
                before=source[source.rfind('\n',0,use.start())+1:use.start()]
                after=source[use.end():]
                if not before.strip() and re.match(r'\s*=(?!=)',after):continue
                raise ValueError('SkillInputByteHasOtherUses')
        aggregate='native_skill_input_'+base
        if re.search(r'\b'+aggregate+r'\b',source):raise ValueError('SkillInputNameCollision')
        replacements += [(decl0.start(),decl0.end(),decl0[1]+TYPE_NAME+' '+aggregate+';\n'),(decl1.start(),decl1.end(),'')]
        replacements += [(a,b,' &'+aggregate) for a,b in spans]
        changes.append(dict(base=base,adjacent=second,aggregate=aggregate,sourceObjectBytes=2,nativeStoreOffsets=[offset,offset+1],
            nativeOffsetEvidence='syntactic STRB offsets only',callerNativeValidationRequired=True,sourceCredit=0))
    result=source
    for start,end,text in sorted(replacements,reverse=True):result=result[:start]+text+result[end:]
    for row in changes:
        result=re.sub(r'\b'+row['base']+r'\b',row['aggregate']+'.skill',result)
        result=re.sub(r'\b'+row['adjacent']+r'\b',row['aggregate']+'.allocated',result)
        result=re.sub(r'(\b'+row['aggregate']+r'\.skill\s*=\s*)\(s8\)',r'\1(u8)',result)
    if Q.TYPE not in result:result=Q.TYPE+'\n'+result
    return result,changes
