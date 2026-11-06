import struct
STEP=[7,8,9,10,11,12,13,14,16,17,19,21,23,25,28,31,34,37,41,45,50,55,60,66,73,80,88,97,107,118,130,143,157,173,190,209,230,253,279,307,337,371,408,449,494,544,598,658,724,796,876,963,1060,1166,1282,1411,1552,1707,1878,2066,2272,2499,2749,3024,3327,3660,4026,4428,4871,5358,5894,6484,7132,7845,8630,9493,10442,11487,12635,13899,15289,16818,18500,20350,22385,24623,27086,29794,32767]
INDEX=[-1,-1,-1,-1,2,4,6,8]


def header(data,magic):
    if len(data)<24:raise ValueError('Truncated Nitro sound member')
    actual,bom,version,size,length,count=struct.unpack_from('<4sHHIHH',data);block,extent=struct.unpack_from('<4sI',data,16)
    if actual!=magic or bom!=0xfeff or version!=0x100 or size!=len(data) or length!=16 or count!=1 or block!=b'DATA' or extent!=size-16:raise ValueError('Nitro sound member exact header/block extent differs')


def wrap(magic,body):return struct.pack('<4sHHIHH4sI',magic,0xfeff,0x100,len(body)+24,16,1,b'DATA',len(body)+8)+body


def pcm(source):
    predictor=source['initialPredictor'];index=source['initialStepIndex'];samples=[predictor]
    if not -32768<=predictor<=32767 or not 0<=index<=88 or not 0<=source['reservedHeaderBits']<512:raise ValueError('ADPCM predictor/index/header-reserved domain differs')
    for token in source['signedQuantizedSteps']:
        if type(token) is not int or token==0 or not -8<=token<=8:raise ValueError('ADPCM signed quantized step must be nonzero -8..8')
        magnitude=abs(token)-1;step=STEP[index];delta=(step>>3)+((step>>2) if magnitude&1 else 0)+((step>>1) if magnitude&2 else 0)+(step if magnitude&4 else 0)
        predictor=max(-32767,min(32767,predictor+(-delta if token<0 else delta)));index=max(0,min(88,index+INDEX[magnitude]));samples.append(predictor)
    return samples


def encode_adpcm(source):
    pcm(source);tokens=source['signedQuantizedSteps']
    if len(tokens)%8:raise ValueError('ADPCM source sample tokens do not form complete stored words')
    nibbles=[(abs(t)-1)|(8 if t<0 else 0) for t in tokens];word=(source['initialPredictor']&65535)|(source['initialStepIndex']<<16)|(source['reservedHeaderBits']<<23)
    return struct.pack('<I',word)+bytes(nibbles[i]|nibbles[i+1]<<4 for i in range(0,len(nibbles),2))


def decode_adpcm(data):
    if len(data)<4 or len(data)%4:raise ValueError('ADPCM initialized sample buffer not word-sized')
    word=struct.unpack_from('<I',data)[0];predictor=word&65535;source=dict(initialPredictor=predictor-65536 if predictor>32767 else predictor,initialStepIndex=word>>16&127,reservedHeaderBits=word>>23,signedQuantizedSteps=[])
    for byte in data[4:]:
        for n in [byte&15,byte>>4]:source['signedQuantizedSteps'].append((-1 if n&8 else 1)*((n&7)+1))
    if encode_adpcm(source)!=data:raise ValueError('ADPCM semantic sample-token roundtrip differs')
    return source


def decode_wave_archive(data):
    header(data,b'SWAR');reserved=list(struct.unpack_from('<8I',data,24));count=struct.unpack_from('<I',data,56)[0]
    if not 1<=count<=1024:raise ValueError('SWAR waveform count out of supported bounds')
    offsets=list(struct.unpack_from('<'+str(count)+'I',data,60));cursor=60+4*count;waves=[]
    for at in offsets:
        if at!=cursor or at+12>len(data):raise ValueError('SWAR waves do not form exact member partition')
        format,loop,rate,timer,start,length=struct.unpack_from('<BB3HI',data,at);end=at+12+4*(start+length)
        if format!=2 or loop not in [0,1] or rate==0 or timer==0 or not 1<=start<start+length or end>len(data):raise ValueError('SWAR ADPCM format/loop/rate/extent differs')
        waves.append(dict(format='Nintendo-DS-ADPCM',looped=bool(loop),sampleRate=rate,timerTicks=timer,loopStartWords=start,loopLengthWords=length,adpcm=decode_adpcm(data[at+12:end])));cursor=end
    if cursor!=len(data):raise ValueError('Unclassified SWAR member suffix')
    source=dict(kind='Nitro-wave-archive',reservedHeaderWords=reserved,waves=waves)
    if encode_wave_archive(source)!=data:raise ValueError('Typed wave archive roundtrip differs')
    return source


def encode_wave_archive(source):
    if source['kind']!='Nitro-wave-archive' or len(source['reservedHeaderWords'])!=8 or not 1<=len(source['waves'])<=1024:raise ValueError('Typed wave archive schema differs')
    chunks=[];offsets=[];at=60+4*len(source['waves'])
    for w in source['waves']:
        samples=encode_adpcm(w['adpcm'])
        if w['format']!='Nintendo-DS-ADPCM' or type(w['looped']) is not bool or not 1<=w['sampleRate']<=65535 or not 1<=w['timerTicks']<=65535 or not 1<=w['loopStartWords']<w['loopStartWords']+w['loopLengthWords'] or len(samples)!=4*(w['loopStartWords']+w['loopLengthWords']):raise ValueError('Typed ADPCM format/parameters/sample extent differs')
        chunk=struct.pack('<BB3HI',2,w['looped'],w['sampleRate'],w['timerTicks'],w['loopStartWords'],w['loopLengthWords'])+samples;offsets.append(at);chunks.append(chunk);at+=len(chunk)
    return wrap(b'SWAR',struct.pack('<8II',*source['reservedHeaderWords'],len(chunks))+struct.pack('<'+str(len(offsets))+'I',*offsets)+b''.join(chunks))


def decode_bank(data):
    header(data,b'SBNK');links=[dict(waveArchivePointer=a,nextLinkPointer=b) for a,b in struct.iter_unpack('<II',data[24:56])];count=struct.unpack_from('<I',data,56)[0];at=60+4*count;instruments=[]
    for value in struct.unpack_from('<'+str(count)+'I',data,60):
        type=value&255;offset=value>>8
        if type not in [1,3] or offset!=at or at+10>len(data):raise ValueError('Unqualified/noncontiguous single-note instrument')
        wave,archive,key,attack,decay,sustain,release,pan=struct.unpack_from('<HH6B',data,at);instruments.append(dict(kind='sample' if type==1 else 'PSG-white-noise',waveIndex=wave,waveArchiveSlot=archive,originalMidiKey=key,attack=attack,decay=decay,sustain=sustain,release=release,pan=pan));at+=10
    if at!=len(data):raise ValueError('Unclassified instrument-bank bytes')
    source=dict(kind='Nitro-instrument-bank',waveArchiveLinks=links,instruments=instruments)
    if encode_bank(source)!=data:raise ValueError('Typed instrument bank roundtrip differs')
    return source


def encode_bank(source):
    if source['kind']!='Nitro-instrument-bank' or len(source['waveArchiveLinks'])!=4 or not 1<=len(source['instruments'])<=128:raise ValueError('Typed instrument-bank schema differs')
    refs=[];chunks=[];at=60+4*len(source['instruments'])
    for i in source['instruments']:
        if i['kind'] not in ['sample','PSG-white-noise'] or not 0<=i['waveArchiveSlot']<4 or not 0<=i['waveIndex']<=65535 or any(not 0<=i[k]<=127 for k in ['originalMidiKey','attack','decay','sustain','release','pan']):raise ValueError('Typed instrument envelope/wave domain differs')
        refs.append((at<<8)|(1 if i['kind']=='sample' else 3));chunks.append(struct.pack('<HH6B',i['waveIndex'],i['waveArchiveSlot'],i['originalMidiKey'],i['attack'],i['decay'],i['sustain'],i['release'],i['pan']));at+=10
    links=b''.join(struct.pack('<II',l['waveArchivePointer'],l['nextLinkPointer']) for l in source['waveArchiveLinks'])
    return wrap(b'SBNK',links+struct.pack('<I',len(refs))+struct.pack('<'+str(len(refs))+'I',*refs)+b''.join(chunks))
