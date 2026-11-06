import re
from wave20261105_child_static_assets_next_formats import encode
from child_message_data_codec_20261106 import encode as encode_lz


def build(document):
    if set(document)!={'version','semantic','compressionRecipe','storageAlignment','measuredZeroAlignmentBytes'} or document['version']!=1 or document['storageAlignment']!=4:raise ValueError('Closed semantic resource document/schema/alignment differs')
    decoded=encode(document['semantic']);payload=encode_lz(decoded,document['compressionRecipe']);alignment=(-len(payload))%4
    if alignment!=document['measuredZeroAlignmentBytes']:raise ValueError('Measured storage alignment differs from source-only encoding')
    return payload,alignment,decoded


def c_source(document,symbol):
    if not re.fullmatch(r'native_child_static_asset_[0-9a-f]{8}',symbol):raise ValueError('Exact typed semantic asset symbol differs')
    payload,alignment,decoded=build(document);size=len(payload)+alignment;lines=['const unsigned char '+symbol+'['+str(size)+'] = {']
    storage=payload+bytes(alignment)
    lines += ['    '+', '.join('0x%02x'%v for v in storage[at:at+32])+',' for at in range(0,len(storage),32)]
    text='\n'.join(lines+['};',''])
    if len(text.splitlines())>500:raise ValueError('Generated resource C exceeds500lines')
    return text,payload+bytes(alignment),len(payload),alignment,len(decoded)
