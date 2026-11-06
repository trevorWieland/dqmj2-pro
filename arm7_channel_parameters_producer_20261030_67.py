import hashlib
from pathlib import Path
import arm7_note_on_native_20261030_60 as original

ROOT=Path(__file__).resolve().parent


def producer():
    raw=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=original.RAW_SHA:
        raise ValueError('Original note caller module changed')
    body=raw[original.ADDRESS-original.memory.BASE:original.ADDRESS-original.memory.BASE+original.SIZE]
    records=[]
    base=original.cases()[0]
    for attack in range(256):
        case=dict(base,type=2,attack=attack,passes=1)
        result=original.execute(body,case,attack)
        state=result['states'][0]
        selected=[row for row in state['actualArgumentWords'] if row[0]==0x037FF8D4]
        if not state['actualReturn'] or state['fault'] is not None or selected!=[[0x037FF8D4,[original.CHANNEL,attack]]]:
            raise ValueError('Actual note caller did not produce the original instrument attack byte')
        if state['actualNestedReturns'].get('0x37ff8d4')!=1:
            raise ValueError('Actual attack nested return missing')
        records.append(dict(attackByte=attack,actualNoteReturn=True,actualAttackReturn=True,
            argumentWords=selected[0][1],nativeStateSha256=hashlib.sha256(repr(result).encode()).hexdigest()))
    first,last=0x038071E0-original.memory.BASE,0x03807273-original.memory.BASE
    return dict(originalCaller=dict(module='arm7-wram',mode='arm',address=hex(original.ADDRESS),bytes=original.SIZE,
            sha256=hashlib.sha256(body).hexdigest(),sourceCredit=0),
        instrumentByteAddress=hex(original.INSTRUMENT+7),actualByteDomain=[0,255],
        actualOriginalNoteReturns=len(records),actualSeparatelyObservedAttackReturns=len(records),
        originalInitializedDataWindow=dict(start='0x38071e0',endExclusive='0x3807273',bytes=147,
            sha256=hashlib.sha256(raw[first:last]).hexdigest(),interiorCoefficientPointer='0x3807260',pointerOffset=128,sourceCredit=0),
        fixtureGenerator=Path(original.__file__).name,fixtureGeneratorSha256=hashlib.sha256(Path(original.__file__).read_bytes()).hexdigest(),
        records=records,providers=[],calleeSourceCredit=0,parentSourceCredit=0,
        limitations=['Actual original note caller and original setter execute; this is producer evidence without new caller source credit',
            'Raw attack128..255 accesses the measured preceding-data window; no instrument-validity meaning is assigned',
            'Positive direct-entry words above255 are outside the declared source data-window contract'])
