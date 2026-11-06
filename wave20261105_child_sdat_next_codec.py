import struct
from wave20261105_child_sdat_next_events import decode as decode_events,encode as encode_events
from wave20261105_child_sdat_next_waves import header,wrap,decode_bank,encode_bank,decode_wave_archive,encode_wave_archive
GROUPS=['sequences','sequenceArchives','banks','waveArchives','players','groups','streamPlayers','streams']


def decode_sequence_archive(data):
    header(data,b'SSAR');base,count=struct.unpack_from('<II',data,24)
    if base!=32+count*12 or not 1<=count<=1024 or base>len(data):raise ValueError('SSAR exact entry table/data base differs')
    commands,positions=decode_events(data[base:]);entries=[]
    for offset,bank,volume,channel,priority,player,reserved in struct.iter_unpack('<IH4BH',data[32:base]):
        if offset!=0xffffffff and offset not in positions:raise ValueError('Sequence entry points into command payload/alignment')
        entries.append(dict(firstEvent=None if offset==0xffffffff else positions[offset],bank=bank,volume=volume,channelPriority=channel,playerPriority=priority,player=player,reservedBits=reserved))
    source=dict(kind='Nitro-sequence-archive',sequences=entries,commands=commands)
    if encode_sequence_archive(source)!=data:raise ValueError('SSAR typed table/event roundtrip differs')
    return source


def encode_sequence_archive(source):
    if source['kind']!='Nitro-sequence-archive' or not 1<=len(source['sequences'])<=1024:raise ValueError('Typed sequence archive schema differs')
    commands=source['commands'];event_data=encode_events(commands)
    from wave20261105_child_sdat_next_events import event_bytes
    offsets={i:0 for i in range(len(commands['events']))};at=0
    for i,event in enumerate(commands['events']):offsets[i]=at;at+=len(event_bytes(event,offsets))
    entries=[]
    for e in source['sequences']:
        if e['firstEvent'] is not None and e['firstEvent'] not in offsets:raise ValueError('Typed sequence entry is not a command boundary')
        if not 0<=e['bank']<=65535 or any(not 0<=e[k]<=127 for k in ['volume','channelPriority','playerPriority']) or not 0<=e['player']<16 or not 0<=e['reservedBits']<=65535:raise ValueError('Sequence bank/priority/player fields differ')
        entries.append(struct.pack('<IH4BH',0xffffffff if e['firstEvent'] is None else offsets[e['firstEvent']],e['bank'],e['volume'],e['channelPriority'],e['playerPriority'],e['player'],e['reservedBits']))
    return wrap(b'SSAR',struct.pack('<II',32+12*len(entries),len(entries))+b''.join(entries)+event_data)


def decode(data):
    if len(data)<64:raise ValueError('Truncated SDAT file header')
    magic,bom,version,size,hs,count=struct.unpack_from('<4sHHIHH',data)
    if (magic,bom,version,size,hs,count)!=(b'SDAT',0xfeff,0x100,len(data),64,3):raise ValueError('SDAT signature/version/declared physical file extent differs')
    descriptors=[struct.unpack_from('<II',data,16+8*i) for i in range(4)];sy,info,fat,file=descriptors
    if sy!=(0,0) or info[0]!=64 or info[0]+info[1]!=fat[0] or fat[0]+fat[1]!=file[0] or file[0]+file[1]!=len(data):raise ValueError('SDAT declared blocks do not exactly partition header/archive')
    for kind,(offset,extent) in zip([b'INFO',b'FAT ',b'FILE'],[info,fat,file]):
        if offset+8>len(data) or struct.unpack_from('<4sI',data,offset)!=(kind,extent):raise ValueError('SDAT actual block header/extent differs')
    group_offsets=struct.unpack_from('<8I',data,info[0]+8);cursor=64;groups={}
    for i,name in enumerate(GROUPS):
        if group_offsets[i]!=cursor:raise ValueError('INFO group tables are noncontiguous or overlap')
        at=info[0]+cursor;number=struct.unpack_from('<I',data,at)[0];refs=struct.unpack_from('<'+str(number)+'I',data,at+4);cursor+=4+4*number;rows=[]
        if number and i not in [1,2,3]:raise ValueError('Unqualified nonempty sound archive INFO group')
        for ref in refs:
            if ref!=cursor:raise ValueError('INFO member record is not an exact typed row')
            start=info[0]+ref;file_id=struct.unpack_from('<I',data,start)[0]
            if i==1:row=dict(fileId=file_id);cursor+=4
            elif i==2:row=dict(fileId=file_id,waveArchives=list(struct.unpack_from('<4H',data,start+4)));cursor+=12
            else:row=dict(fileId=file_id&0xffffff,flags=file_id>>24);cursor+=4
            rows.append(row)
        groups[name]=rows
    if cursor!=info[1]:raise ValueError('Unclassified INFO block bytes')
    n=struct.unpack_from('<I',data,fat[0]+8)[0]
    if not 1<=n<=1024 or fat[1]!=12+16*n or struct.unpack_from('<I',data,file[0]+8)[0]!=n:raise ValueError('SDAT FAT/FILE declared member count/extent differs')
    files=[];cursor=file[0]+12;padding=[]
    for i in range(n):
        at,size,memory,reserved=struct.unpack_from('<4I',data,fat[0]+12+16*i)
        if at!=(cursor+31)&~31 or at+size>len(data) or any(data[cursor:at]):raise ValueError('SDAT member/FAT exact extent or measured zero alignment differs')
        blob=data[at:at+size];kind=blob[:4];codec={b'SSAR':decode_sequence_archive,b'SBNK':decode_bank,b'SWAR':decode_wave_archive}.get(kind)
        if codec is None:raise ValueError('Unqualified SDAT member signature')
        files.append(dict(kind=kind.decode(),memoryPointer=memory,reservedWord=reserved,semantic=codec(blob)));padding.append(at-cursor);cursor=at+size
    if len(data)!=(cursor+31)&~31 or any(data[cursor:]):raise ValueError('SDAT terminal zero alignment differs')
    source=dict(version=1,kind='Nitro-sound-archive',headerReservedWords=list(struct.unpack_from('<4I',data,48)),infoReservedWords=list(struct.unpack_from('<6I',data,info[0]+40)),fileAlignment=32,info=groups,files=files)
    if encode(source)!=data:raise ValueError('Complete typed sound archive encode differs')
    return source,dict(memberPaddingBytes=padding,terminalPaddingBytes=len(data)-cursor,typedMembers=n)


def encode(source):
    if source['version']!=1 or source['kind']!='Nitro-sound-archive' or source['fileAlignment']!=32 or len(source['headerReservedWords'])!=4 or len(source['infoReservedWords'])!=6:raise ValueError('Typed SDAT schema/alignment differs')
    groups=source['info'];files=source['files'];blobs=[]
    if set(groups)!=set(GROUPS) or not 1<=len(files)<=1024:raise ValueError('Typed INFO/member count differs')
    for file in files:
        encoder={'SSAR':encode_sequence_archive,'SBNK':encode_bank,'SWAR':encode_wave_archive}.get(file['kind'])
        if encoder is None:raise ValueError('Unqualified typed SDAT member')
        blobs.append(encoder(file['semantic']))
    lists=[];offsets=[];cursor=64
    for i,name in enumerate(GROUPS):
        rows=groups[name];offsets.append(cursor);record_start=cursor+4+4*len(rows);refs=[];records=[]
        if rows and i not in [1,2,3]:raise ValueError('Unqualified typed INFO group')
        for row in rows:
            index=row['fileId']
            if not 0<=index<len(files) or files[index]['kind']!={1:'SSAR',2:'SBNK',3:'SWAR'}[i]:raise ValueError('INFO file reference kind/index differs')
            refs.append(record_start)
            if i==1:record=struct.pack('<I',index)
            elif i==2:
                if len(row['waveArchives'])!=4 or any(x!=65535 and not 0<=x<len(groups['waveArchives']) for x in row['waveArchives']):raise ValueError('Instrument bank wave-archive reference differs')
                record=struct.pack('<I4H',index,*row['waveArchives'])
            else:
                if not 0<=row['flags']<=255:raise ValueError('Wave archive INFO flag domain differs')
                record=struct.pack('<I',index|row['flags']<<24)
            records.append(record);record_start+=len(record)
        chunk=struct.pack('<I',len(rows))+struct.pack('<'+str(len(refs))+'I',*refs)+b''.join(records);lists.append(chunk);cursor+=len(chunk)
    info=struct.pack('<4sI8I6I',b'INFO',cursor,*offsets,*source['infoReservedWords'])+b''.join(lists);fat_at=64+len(info);fat_size=12+16*len(files);file_at=fat_at+fat_size;payload=bytearray(struct.pack('<4sII',b'FILE',0,len(files)));fat_rows=[]
    for file,blob in zip(files,blobs):
        payload.extend(bytes((-(file_at+len(payload)))%32));fat_rows.append(struct.pack('<4I',file_at+len(payload),len(blob),file['memoryPointer'],file['reservedWord']));payload.extend(blob)
    payload.extend(bytes((-(file_at+len(payload)))%32));struct.pack_into('<I',payload,4,len(payload));fat=struct.pack('<4sII',b'FAT ',fat_size,len(files))+b''.join(fat_rows);size=file_at+len(payload)
    result=struct.pack('<4sHHIHH8I4I',b'SDAT',0xfeff,0x100,size,64,3,0,0,64,len(info),fat_at,len(fat),file_at,len(payload),*source['headerReservedWords'])+info+fat+payload
    validate_cross_references(source);return result


def validate_cross_references(source):
    groups=source['info']
    for file in source['files']:
        s=file['semantic']
        if file['kind']=='SSAR':
            for entry in s['sequences']:
                if not 0<=entry['bank']<len(groups['banks']):raise ValueError('SSAR entry bank reference differs')
            for event in s['commands']['events']:
                if event['kind']=='program' and (not 0<=event['bank']<len(groups['banks']) or event['instrument']>=len(source['files'][groups['banks'][event['bank']]['fileId']]['semantic']['instruments'])):raise ValueError('MML program selects absent instrument/bank')
        elif file['kind']=='SBNK':
            indexes=[i for i,r in enumerate(groups['banks']) if source['files'][r['fileId']] is file]
            if len(indexes)!=1:raise ValueError('Instrument-bank INFO ownership ambiguous')
            mapping=groups['banks'][indexes[0]]['waveArchives']
            for instrument in s['instruments']:
                if instrument['kind']=='sample':
                    index=mapping[instrument['waveArchiveSlot']]
                    if index==65535 or not 0<=index<len(groups['waveArchives']):raise ValueError('Instrument selects absent wave-archive slot')
                    waves=source['files'][groups['waveArchives'][index]['fileId']]['semantic']['waves']
                    if not 0<=instrument['waveIndex']<len(waves):raise ValueError('Instrument selects absent waveform')
