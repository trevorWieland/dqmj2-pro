import struct


def pointer_index(pointer,blocks,kind):
    if not pointer:return None
    matches=[i for i,b in enumerate(blocks) if b['offset']+8==pointer and b['kind']==kind]
    if len(matches)!=1:raise ValueError('NFTR relative pointer does not address exact typed block body')
    return matches[0]


def decode_font(header,blocks):
    sections=[]
    for block in blocks:
        kind=block['kind'];raw=block['payload']
        if kind=='FNIF':
            if len(raw)!=20:raise ValueError('NFTR FINF extent differs')
            typ,line,alternate,left,width,advance,encoding,glyph,widths,maps=struct.unpack('<BbHbBbBIII',raw)
            if typ!=0 or encoding not in [0,1,2,3]:raise ValueError('NFTR glyph type/encoding unsupported')
            sections.append(dict(kind='font-information',fontType=typ,lineFeed=line,alternateGlyph=alternate,defaultWidth=dict(left=left,glyphWidth=width,charAdvance=advance),encoding=encoding,glyphBlock=pointer_index(glyph,blocks,'PLGC'),widthBlock=pointer_index(widths,blocks,'HDWC'),mapBlock=pointer_index(maps,blocks,'PAMC')))
        elif kind=='PLGC':
            if len(raw)<8:raise ValueError('NFTR glyph header truncated')
            width,height,cell,baseline,maxWidth,bpp,flags=struct.unpack_from('<BBHbBBB',raw);bits=width*height*bpp;unused=cell*8-bits
            if not width or not height or not 1<=bpp<=4 or not 0<=unused<8 or (len(raw)-8)%cell:raise ValueError('NFTR glyph dimensions/cell extent/bitdepth differ')
            glyphs=[]
            for at in range(8,len(raw),cell):
                word=int.from_bytes(raw[at:at+cell],'big');pixels=[word>>(cell*8-(n+1)*bpp)&((1<<bpp)-1) for n in range(width*height)];glyphs.append(dict(rows=[''.join(format(p,'x') for p in pixels[y*width:y*width+width]) for y in range(height)],unusedCellBits=word&((1<<unused)-1)))
            sections.append(dict(kind='glyph-bitmap',width=width,height=height,cellBytes=cell,baseline=baseline,maxCharWidth=maxWidth,bitsPerPixel=bpp,verticalOrder=bool(flags&1),rotation=flags>>1&3,unknownFlags=flags&~7,glyphs=glyphs))
        elif kind=='HDWC':
            if len(raw)<8:raise ValueError('NFTR width header truncated')
            first,last,nextPointer=struct.unpack_from('<HHI',raw);count=last-first+1;end=8+count*3
            if count<=0 or end>len(raw) or len(raw)-end>3:raise ValueError('NFTR character-width index range/extent differs')
            widths=[dict(left=a,glyphWidth=b,charAdvance=c) for a,b,c in struct.iter_unpack('<bBb',raw[8:end])];sections.append(dict(kind='character-widths',firstGlyph=first,lastGlyph=last,nextBlock=pointer_index(nextPointer,blocks,'HDWC'),widths=widths,paddingBytes=list(raw[end:])))
        elif kind=='PAMC':
            if len(raw)<12:raise ValueError('NFTR character map truncated')
            first,last,method,reserved,nextPointer=struct.unpack_from('<HHHHI',raw);at=12;mapping=None
            if method==0:
                if at+2>len(raw):raise ValueError('NFTR direct map truncated')
                mapping=dict(firstGlyph=struct.unpack_from('<H',raw,at)[0]);at+=2
            elif method==1:
                count=last-first+1;end=at+2*count
                if count<=0 or end>len(raw):raise ValueError('NFTR table map range/extent differs')
                mapping=dict(glyphIndices=[None if i==65535 else i for (i,) in struct.iter_unpack('<H',raw[at:end])]);at=end
            elif method==2:
                if at+2>len(raw):raise ValueError('NFTR scan count truncated')
                count=struct.unpack_from('<H',raw,at)[0];at+=2;end=at+count*4
                if end>len(raw):raise ValueError('NFTR scan entries truncated')
                mapping=dict(entries=[dict(codePoint=a,glyph=b) for a,b in struct.iter_unpack('<HH',raw[at:end])]);at=end
            else:raise ValueError('Unsupported NFTR code-map method')
            if len(raw)-at>3:raise ValueError('NFTR code-map contains unclassified payload')
            sections.append(dict(kind='character-map',firstCodePoint=first,lastCodePoint=last,method=method,reservedBits=reserved,nextBlock=pointer_index(nextPointer,blocks,'PAMC'),mapping=mapping,paddingBytes=list(raw[at:])))
        else:raise ValueError('Unqualified NFTR block: '+kind)
    if sum(s['kind']=='font-information' for s in sections)!=1 or sum(s['kind']=='glyph-bitmap' for s in sections)!=1:raise ValueError('NFTR requires unique information/glyph sections')
    info=next(s for s in sections if s['kind']=='font-information');glyph=next(s for s in sections if s['kind']=='glyph-bitmap');glyphCount=len(glyph['glyphs'])
    if info['alternateGlyph']>=glyphCount or info['glyphBlock'] is None:raise ValueError('Font fallback glyph/typed glyph link outside bitmap array')
    for section in sections:
        if section['kind']=='character-widths' and not 0<=section['firstGlyph']<=section['lastGlyph']<glyphCount:raise ValueError('Font width indices escape glyph array')
        if section['kind']=='character-map':
            mapping=section['mapping'];method=section['method']
            indices=[e['glyph'] for e in mapping['entries']] if method==2 else [i for i in mapping['glyphIndices'] if i is not None] if method==1 else list(range(mapping['firstGlyph'],mapping['firstGlyph']+section['lastCodePoint']-section['firstCodePoint']+1))
            if any(not 0<=i<glyphCount for i in indices):raise ValueError('Character map references unavailable glyph')
            if method==2 and any(not section['firstCodePoint']<=e['codePoint']<=section['lastCodePoint'] for e in mapping['entries']):raise ValueError('Sparse character map code point escapes declared range')
    for first,kind in [(info['widthBlock'],'character-widths'),(info['mapBlock'],'character-map')]:
        seen=set();index=first
        while index is not None:
            if index in seen or not 0<=index<len(sections) or sections[index]['kind']!=kind:raise ValueError('Font typed block list cycle/type mismatch')
            seen.add(index);index=sections[index]['nextBlock']
        if seen!={i for i,s in enumerate(sections) if s['kind']==kind}:raise ValueError('Font contains unreachable width/code-map block')
    return dict(version=1,kind='Nitro-font-glyphs',header=header,sections=sections)


def encode_font(source):
    from wave20261105_child_static_assets_next_formats import wrap,decode
    sections=source['sections'];offsets=[];blocks=[];links=[];cursor=16
    for section in sections:
        kind=section['kind'];payload=bytearray();pending=[]
        if kind=='font-information':
            d=section['defaultWidth'];payload+=struct.pack('<BbHbBbBIII',section['fontType'],section['lineFeed'],section['alternateGlyph'],d['left'],d['glyphWidth'],d['charAdvance'],section['encoding'],0,0,0);pending=[(8,section['glyphBlock'],'PLGC'),(12,section['widthBlock'],'HDWC'),(16,section['mapBlock'],'PAMC')];signature='FNIF'
        elif kind=='glyph-bitmap':
            width,height,cell,bpp=section['width'],section['height'],section['cellBytes'],section['bitsPerPixel'];unused=cell*8-width*height*bpp;flags=int(section['verticalOrder'])|section['rotation']<<1|section['unknownFlags']
            if not 1<=bpp<=4 or not 0<=unused<8 or not 0<=flags<256:raise ValueError('Invalid semantic glyph bit/flag domains')
            payload+=struct.pack('<BBHbBBB',width,height,cell,section['baseline'],section['maxCharWidth'],bpp,flags)
            for glyph in section['glyphs']:
                if len(glyph['rows'])!=height or any(len(r)!=width for r in glyph['rows']):raise ValueError('Glyph raster dimensions differ')
                word=0
                for row in glyph['rows']:
                    for value in row:
                        pixel=int(value,16)
                        if pixel>=1<<bpp:raise ValueError('Glyph pixel exceeds bit-depth domain')
                        word=word<<bpp|pixel
                if not 0<=glyph['unusedCellBits']<1<<unused:raise ValueError('Unused glyph-cell bits overflow')
                payload+=(word<<unused|glyph['unusedCellBits']).to_bytes(cell,'big')
            signature='PLGC'
        elif kind=='character-widths':
            if len(section['widths'])!=section['lastGlyph']-section['firstGlyph']+1:raise ValueError('Character-width count differs')
            payload+=struct.pack('<HHI',section['firstGlyph'],section['lastGlyph'],0);pending=[(4,section['nextBlock'],'HDWC')]
            for d in section['widths']:payload+=struct.pack('<bBb',d['left'],d['glyphWidth'],d['charAdvance'])
            payload+=bytes(section['paddingBytes']);signature='HDWC'
        elif kind=='character-map':
            first,last,method=section['firstCodePoint'],section['lastCodePoint'],section['method'];payload+=struct.pack('<HHHHI',first,last,method,section['reservedBits'],0);pending=[(8,section['nextBlock'],'PAMC')];mapping=section['mapping']
            if method==0:payload+=struct.pack('<H',mapping['firstGlyph'])
            elif method==1:
                if len(mapping['glyphIndices'])!=last-first+1:raise ValueError('Table character-map count differs')
                payload+=b''.join(struct.pack('<H',65535 if i is None else i) for i in mapping['glyphIndices'])
            elif method==2:
                entries=mapping['entries'];payload+=struct.pack('<H',len(entries));payload+=b''.join(struct.pack('<HH',e['codePoint'],e['glyph']) for e in entries)
            else:raise ValueError('Unsupported semantic character-map method')
            payload+=bytes(section['paddingBytes']);signature='PAMC'
        else:raise ValueError('Unknown semantic font section')
        offsets.append(cursor+8);blocks.append((signature,payload));links.append(pending);cursor+=8+len(payload)
    for i,pending in enumerate(links):
        for at,index,kind in pending:
            if index is not None and (not 0<=index<len(blocks) or blocks[index][0]!=kind):raise ValueError('Semantic font link has wrong block index/type')
            struct.pack_into('<I',blocks[i][1],at,0 if index is None else offsets[index])
    result=wrap(source['header'],blocks)
    if decode(result)!=source:raise ValueError('Semantic NFTR encode/decode differs')
    return result
