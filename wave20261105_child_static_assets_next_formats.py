import struct


def common(data):
    if len(data)<16:raise ValueError('Truncated Nitro binary header')
    magic,bom,version,size,header,count=struct.unpack_from('<4sHHIHH',data)
    if magic not in [b'RGCN',b'RLCN',b'RCSN',b'RTFN'] or bom!=0xfeff or version not in [0x100,0x101] or size!=len(data) or header!=16 or not 1<=count<=64:raise ValueError('Nitro binary signature/endian/version/file extent differs')
    blocks=[];at=header
    for i in range(count):
        if at+8>len(data):raise ValueError('Truncated Nitro block header')
        kind,extent=struct.unpack_from('<4sI',data,at)
        if extent<8 or at+extent>len(data):raise ValueError('Nitro block extent escapes declared file')
        blocks.append(dict(kind=kind.decode('ascii'),offset=at,payload=data[at+8:at+extent]));at+=extent
    if at!=len(data):raise ValueError('Nitro blocks do not exactly partition file')
    return dict(magic=magic.decode(),byteOrder=bom,version=version),blocks


def wrap(header,blocks):
    payload=b''.join(kind.encode('ascii')+struct.pack('<I',len(data)+8)+data for kind,data in blocks)
    return struct.pack('<4sHHIHH',header['magic'].encode(),header['byteOrder'],header['version'],16+len(payload),16,len(blocks))+payload


def decode(data):
    header,blocks=common(data)
    if header['magic']=='RTFN':
        from wave20261105_child_static_assets_next_font import decode_font
        return decode_font(header,blocks)
    extra=None
    if len(blocks)==2 and header['magic']=='RGCN' and blocks[1]['kind']=='SOPC' and len(blocks[1]['payload'])==8:
        x,y,w,h=struct.unpack('<4H',blocks[1]['payload']);extra=dict(sourceX=x,sourceY=y,sourceWidth=w,sourceHeight=h)
    elif len(blocks)!=1:raise ValueError('Unqualified additional Nitro2D section')
    block=blocks[0];raw=block['payload'];magic=header['magic']
    if magic=='RGCN':
        if block['kind']!='RAHC' or len(raw)<24:raise ValueError('NCGR character section missing')
        height,width,pixel,mapping,formatWord,size,offset=struct.unpack_from('<HHIIIII',raw)
        if pixel!=3 or offset!=24 or size!=len(raw)-24 or size%32 or height*width!=size//32:raise ValueError('NCGR 4bpp tile geometry/format/relative data extent differs')
        tiles=[]
        for at in range(24,len(raw),32):
            pixels=[n for byte in raw[at:at+32] for n in [byte&15,byte>>4]];tiles.append([''.join(format(x,'x') for x in pixels[y*8:y*8+8]) for y in range(8)])
        return dict(version=1,kind='Nitro2D-4bpp-tiles',header=header,heightTiles=height,widthTiles=width,pixelFormat=pixel,mappingTypeWord=mapping,characterFormat=formatWord&255,vramTransfer=bool(formatWord&256),unknownCharacterFlags=formatWord&~511,tiles=tiles,position=extra)
    if magic=='RLCN':
        if block['kind']!='TTLP' or len(raw)<16:raise ValueError('NCLR palette section missing')
        pixel,extended,size,offset=struct.unpack_from('<IIII',raw)
        if pixel!=3 or offset!=16 or size!=len(raw)-16 or size%2:raise ValueError('NCLR format/relative palette extent differs')
        colors=[]
        for (word,) in struct.iter_unpack('<H',raw[16:]):colors.append(dict(r5=word&31,g5=word>>5&31,b5=word>>10&31,unusedBit15=word>>15))
        return dict(version=1,kind='Nitro2D-RGB555-palette',header=header,pixelFormat=pixel,extendedPaletteWord=extended,colors=colors)
    if magic=='RCSN':
        if block['kind']!='NRCS' or len(raw)<12:raise ValueError('NSCR screen section missing')
        width,height,colorMode,screenFormat,size=struct.unpack_from('<HHHHI',raw)
        if width%8 or height%8 or colorMode!=0 or screenFormat!=0 or size!=len(raw)-12 or size!=width*height//32:raise ValueError('NSCR text-mode tile map dimensions/format/extent differ')
        cells=[]
        for (word,) in struct.iter_unpack('<H',raw[12:]):cells.append(dict(tile=word&1023,horizontalFlip=bool(word&1024),verticalFlip=bool(word&2048),palette=word>>12))
        return dict(version=1,kind='Nitro2D-text-screen',header=header,widthPixels=width,heightPixels=height,colorMode=colorMode,screenFormat=screenFormat,rows=[cells[i:i+width//8] for i in range(0,len(cells),width//8)])
    raise ValueError('Unqualified semantic Nitro format')


def encode(source):
    if source['version']!=1:raise ValueError('Unsupported semantic source version')
    if source['kind']=='Nitro-font-glyphs':
        from wave20261105_child_static_assets_next_font import encode_font
        return encode_font(source)
    kind=source['kind'];header=source['header'];raw=bytearray()
    if kind=='Nitro2D-4bpp-tiles':
        if header['magic']!='RGCN' or source['pixelFormat']!=3 or len(source['tiles'])!=source['heightTiles']*source['widthTiles']:raise ValueError('Semantic NCGR tile geometry differs')
        for tile in source['tiles']:
            if len(tile)!=8 or any(len(row)!=8 or any(c not in '0123456789abcdef' for c in row) for row in tile):raise ValueError('Tile must contain8x8 editable4bpp pixels')
            values=[int(c,16) for row in tile for c in row];raw.extend(values[i]|values[i+1]<<4 for i in range(0,64,2))
        flags=source['characterFormat']|int(source['vramTransfer'])<<8|source['unknownCharacterFlags']
        payload=struct.pack('<HHIIIII',source['heightTiles'],source['widthTiles'],3,source['mappingTypeWord'],flags,len(raw),24)+raw;blocks=[('RAHC',payload)]
        if source['position'] is not None:
            p=source['position'];blocks.append(('SOPC',struct.pack('<4H',p['sourceX'],p['sourceY'],p['sourceWidth'],p['sourceHeight'])))
    elif kind=='Nitro2D-RGB555-palette':
        if header['magic']!='RLCN' or source['pixelFormat']!=3:raise ValueError('Semantic palette type differs')
        for color in source['colors']:
            if any(not 0<=color[c]<=31 for c in ['r5','g5','b5']) or color['unusedBit15'] not in [0,1]:raise ValueError('Palette components exceed RGB555/unused-bit domain')
            raw+=struct.pack('<H',color['r5']|color['g5']<<5|color['b5']<<10|color['unusedBit15']<<15)
        blocks=[('TTLP',struct.pack('<IIII',3,source['extendedPaletteWord'],len(raw),16)+raw)]
    elif kind=='Nitro2D-text-screen':
        width,height=source['widthPixels'],source['heightPixels']
        if header['magic']!='RCSN' or width%8 or height%8 or len(source['rows'])!=height//8 or any(len(r)!=width//8 for r in source['rows']):raise ValueError('Semantic screen geometry differs')
        for row in source['rows']:
            for cell in row:
                if not 0<=cell['tile']<1024 or not 0<=cell['palette']<16 or type(cell['horizontalFlip']) is not bool or type(cell['verticalFlip']) is not bool:raise ValueError('Map cell exceeds tile/flip/palette domains')
                raw+=struct.pack('<H',cell['tile']|int(cell['horizontalFlip'])<<10|int(cell['verticalFlip'])<<11|cell['palette']<<12)
        blocks=[('NRCS',struct.pack('<HHHHI',width,height,source['colorMode'],source['screenFormat'],len(raw))+raw)]
    else:raise ValueError('Unknown semantic source kind')
    result=wrap(header,blocks)
    if decode(result)!=source:raise ValueError('Semantic Nitro2D encode/decode contract differs')
    return result
