import builtins
import io
import os
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
from project import ROOT,read_json,sha256
import match_runtime as C
from wave20261105_child_sdat_next_source_codec import c_source
SOURCE=ROOT/'src/utility/parallel_wave20261105/child-sdat-next'
LAYOUT=SOURCE/'layout.json'
LAYOUT_HASH='a94bb11438051eaf7b73977441dc234e640ab4099bede38c42ecc9424ac43182'


@contextmanager
def source_only():
    reads=[];builtin=builtins.open;iopen=io.open;opener=os.open
    def check(path):
        if isinstance(path,int):raise PermissionError('Raw descriptors forbidden during source-only asset generation')
        resolved=Path(path).resolve()
        if not resolved.is_relative_to(SOURCE.resolve()):raise PermissionError('Original/extracted/other external reads blocked during semantic source generation')
        reads.append(resolved.relative_to(ROOT).as_posix())
    def guarded_builtin(path,*args,**kwargs):check(path);return builtin(path,*args,**kwargs)
    def guarded_io(path,*args,**kwargs):check(path);return iopen(path,*args,**kwargs)
    def guarded_os(path,*args,**kwargs):check(path);return opener(path,*args,**kwargs)
    with patch.object(builtins,'open',guarded_builtin),patch.object(io,'open',guarded_io),patch.object(os,'open',guarded_os):yield reads


def generate(layout):
    if SOURCE!=ROOT/'src/utility/parallel_wave20261105/child-sdat-next' or (layout['program'],layout['processor'],layout['module'],layout['base'])!=('dwc/utility.bin/move/child.srl','arm9','utility-child-arm9-main','0x2000000'):raise ValueError('Exact isolated semantic resource namespace/base differs')
    if layout['inputModuleSha256']!='af25c028552d9de7428f5393757507b3c029e80f22c9cc44e94e45103f0814d0' or layout['binary']!='extract/utility/runtime/utility-child-arm9-main.bin':raise ValueError('Original initialized comparison identity differs')
    values=[]
    for asset in layout['assets']:
        path=(ROOT/asset['semanticSource']).resolve();address=int(asset['address'],0)
        if not path.is_relative_to(SOURCE.resolve()) or path.name!=format(address,'08x')+'.json' or sha256(path)!=asset['semanticSourceSha256']:raise ValueError('Pinned canonical semantic input path/hash differs')
        symbol='native_child_sound_asset_'+format(address,'08x');document=read_json(path);text,payload,encoded,padding,decoded=c_source(document,symbol)
        if len(payload)!=asset['bytes'] or encoded!=asset['encodedAssetBytes'] or padding!=asset['measuredZeroAlignmentBytes'] or C.sha(payload)!=asset['targetSha256'] or document['semantic']['kind']!='Nitro-sound-archive' or asset['formatKind']!='Nitro-SDAT/SSAR/SBNK/SWAR-ADPCM':raise ValueError('Complete semantic storage/scalar/format hash differs')
        values.append((asset,symbol,text,payload,decoded))
    if len(values)!=1 or sum(len(r[3]) for r in values)!=13936 or sum(r[0]['measuredZeroAlignmentBytes'] for r in values)!=1:raise ValueError('Exact1/13936semantic sound resource source scope differs')
    return values


def original_read_controls(config,layout):
    denied=[]
    for path in [ROOT/config['rom'],ROOT/layout['binary'],ROOT/'extract/files/dwc/utility.bin']:
        methods=[('Path.read_bytes',lambda p=path:p.read_bytes()),('builtins.open',lambda p=path:builtins.open(p,'rb')),('io.open',lambda p=path:io.open(p,'rb')),('os.open',lambda p=path:os.open(p,os.O_RDONLY))]
        for name,operation in methods:
            try:operation()
            except PermissionError as error:denied.append(dict(method=name,path=path.relative_to(ROOT).as_posix(),rejected=True,reason=str(error)))
            else:raise ValueError('Original input read route remained open during semantic generation')
    return denied
