import struct


def variable(value):
    if not isinstance(value,int) or not 0<=value<0x10000000:raise ValueError('MML variable-length argument escapes28bits')
    result=[value&127];value>>=7
    while value:result.insert(0,(value&127)|128);value>>=7
    return bytes(result)


def event_bytes(event,offsets):
    kind=event['kind']
    if kind=='note':
        if not 0<=event['midiNote']<=127 or not 0<=event['velocity']<=127 or type(event['velocityHighBit']) is not bool:raise ValueError('MML note/velocity/flag domain differs')
        return bytes([event['midiNote'],event['velocity']|(128 if event['velocityHighBit'] else 0)])+variable(event['ticks'])
    if kind=='wait':return b'\x80'+variable(event['ticks'])
    if kind=='program':
        if not 0<=event['instrument']<=127 or not 0<=event['bank']<=511:raise ValueError('MML program bank/instrument domain differs')
        return b'\x81'+variable(event['bank']*128+event['instrument'])
    if kind in ['open-track','jump','call']:
        if event['target'] not in offsets:raise ValueError('MML branch is not an exact declared event entry')
        target=offsets[event['target']].to_bytes(3,'little')
        if kind=='open-track':
            if not 0<=event['track']<16:raise ValueError('MML track index escapes16tracks')
            return bytes([0x93,event['track']])+target
        return bytes([0x94 if kind=='jump' else 0x95])+target
    if kind in ['pan','pitch-bend','portamento-key','portamento-enabled']:
        value=event['value'];code={'pan':0xc0,'pitch-bend':0xc4,'portamento-key':0xc9,'portamento-enabled':0xce}[kind]
        if kind=='pitch-bend':
            if not -128<=value<=127:raise ValueError('MML signed pitch-bend domain differs')
            value&=255
        elif not 0<=value<=(1 if kind=='portamento-enabled' else 127):raise ValueError('MML controller argument domain differs')
        return bytes([code,value])
    if kind=='allocate-tracks':
        tracks=event['tracks']
        if len(tracks)!=len(set(tracks)) or any(not 0<=x<16 for x in tracks):raise ValueError('MML track allocation indices differ')
        return b'\xfe'+sum(1<<x for x in tracks).to_bytes(2,'little')
    if kind in ['return','finish']:return bytes([0xfd if kind=='return' else 0xff])
    raise ValueError('Unqualified MML command kind')


def decode(data):
    events=[];positions={};at=0
    while at<len(data):
        if len(data)-at<3 and not any(data[at:]) and events and events[-1]['kind']=='finish':break
        start=at;code=data[at];at+=1
        def byte():
            nonlocal at
            if at>=len(data):raise ValueError('Truncated MML command')
            value=data[at];at+=1;return value
        def var():
            start=at;value=0
            for i in range(4):
                b=byte();value=value*128+(b&127)
                if not b&128:
                    if data[start:at]!=variable(value):raise ValueError('Noncanonical MML variable-length argument')
                    return value
            raise ValueError('Overlong MML argument')
        if code<128:
            velocity=byte();event=dict(kind='note',midiNote=code,velocity=velocity&127,velocityHighBit=bool(velocity&128),ticks=var())
        elif code==0x80:event=dict(kind='wait',ticks=var())
        elif code==0x81:
            program=var();event=dict(kind='program',bank=program>>7,instrument=program&127)
        elif code in [0x93,0x94,0x95]:
            event=dict(kind={0x93:'open-track',0x94:'jump',0x95:'call'}[code])
            if code==0x93:event['track']=byte()
            event['targetOffset']=byte()|byte()<<8|byte()<<16
        elif code in [0xc0,0xc4,0xc9,0xce]:
            value=byte();event=dict(kind={0xc0:'pan',0xc4:'pitch-bend',0xc9:'portamento-key',0xce:'portamento-enabled'}[code],value=value-256 if code==0xc4 and value>127 else value)
        elif code==0xfe:
            flags=byte()|byte()<<8;event=dict(kind='allocate-tracks',tracks=[i for i in range(16) if flags>>i&1])
        elif code in [0xfd,0xff]:event=dict(kind='return' if code==0xfd else 'finish')
        else:raise ValueError('Unqualified MML opcode '+hex(code))
        positions[start]=len(events);events.append(event)
    for event in events:
        if 'targetOffset' in event:
            target=event.pop('targetOffset')
            if target not in positions:raise ValueError('MML target enters command payload/padding')
            event['target']=positions[target]
    source=dict(events=events,measuredZeroAlignmentBytes=len(data)-at)
    if encode(source)!=data:raise ValueError('Typed MML event roundtrip differs')
    return source,positions


def encode(source):
    events=source['events'];offsets={i:0 for i in range(len(events))};at=0
    for i,event in enumerate(events):offsets[i]=at;at+=len(event_bytes(event,offsets))
    body=b''.join(event_bytes(event,offsets) for event in events);pad=source['measuredZeroAlignmentBytes']
    if not 0<=pad<=2 or (-len(body))%4!=pad:raise ValueError('MML measured terminal alignment differs')
    return body+bytes(pad)
