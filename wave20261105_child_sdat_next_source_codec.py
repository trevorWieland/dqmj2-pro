import re
from wave20261105_child_sdat_next_codec import encode
from child_message_data_codec_20261106 import encode as encode_lz


def build(document):
    if set(document)!={'version','semantic','compressionRecipe','storageAlignment','measuredZeroAlignmentBytes'} or document['version']!=1 or document['storageAlignment']!=4:raise ValueError('Closed typed sound source schema/alignment differs')
    decoded=encode(document['semantic']);payload=encode_lz(decoded,document['compressionRecipe']);alignment=(-len(payload))%4
    if alignment!=document['measuredZeroAlignmentBytes']:raise ValueError('Measured sound storage alignment differs from source-only encoding')
    return payload,alignment,decoded


def c_source(document,symbol):
    if symbol!='native_child_sound_asset_0201c140':raise ValueError('Exact admitted typed sound symbol differs')
    payload,alignment,decoded=build(document);storage=payload+bytes(alignment);lines=['const unsigned char '+symbol+'['+str(len(storage))+'] = {'];lines+=['    '+', '.join('0x%02x'%v for v in storage[at:at+32])+',' for at in range(0,len(storage),32)];text='\n'.join(lines+['};',''])
    if len(text.splitlines())>500:raise ValueError('Generated sound resource C exceeds500lines')
    return text,storage,len(payload),alignment,len(decoded)
