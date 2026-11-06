import builtins
import io
import os
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
from project import ROOT,read_json,sha256
import match_runtime as C
from wave20261105_child_static_assets_next_source_codec import c_source
import wave20261105_child_static_assets_next_font
SOURCE=ROOT/'src/utility/parallel_wave20261105/child-static-assets-next'
LAYOUT=SOURCE/'layout.json'
LAYOUT_HASH='21b3fc32eae705033fa07c3e0a6ede164e6b7a1315838988efee6ff55b804f01'


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
    if SOURCE!=ROOT/'src/utility/parallel_wave20261105/child-static-assets-next' or (layout['program'],layout['processor'],layout['module'],layout['base'])!=('dwc/utility.bin/move/child.srl','arm9','utility-child-arm9-main','0x2000000'):raise ValueError('Exact isolated semantic resource namespace/base differs')
    if layout['inputModuleSha256']!='af25c028552d9de7428f5393757507b3c029e80f22c9cc44e94e45103f0814d0' or layout['binary']!='extract/utility/runtime/utility-child-arm9-main.bin':raise ValueError('Original initialized comparison identity differs')
    values=[]
    for asset in layout['assets']:
        path=(ROOT/asset['semanticSource']).resolve();address=int(asset['address'],0)
        if not path.is_relative_to(SOURCE.resolve()) or path.name!=format(address,'08x')+'.json' or sha256(path)!=asset['semanticSourceSha256']:raise ValueError('Pinned canonical semantic input path/hash differs')
        symbol='native_child_static_asset_'+format(address,'08x');document=read_json(path);text,payload,encoded,padding,decoded=c_source(document,symbol)
        if len(payload)!=asset['bytes'] or encoded!=asset['encodedAssetBytes'] or padding!=asset['measuredZeroAlignmentBytes'] or C.sha(payload)!=asset['targetSha256'] or document['semantic']['kind']!=asset['formatKind']:raise ValueError('Complete semantic storage/scalar/format hash differs')
        values.append((asset,symbol,text,payload,decoded))
    if len(values)!=37 or sum(len(r[3]) for r in values)!=50456 or sum(r[0]['measuredZeroAlignmentBytes'] for r in values)!=54:raise ValueError('Exact37/50456semantic resource source scope differs')
    return values


def original_read_controls(config,layout):
    denied=[]
    for path in [ROOT/config['rom'],ROOT/layout['binary']]:
        methods=[('Path.read_bytes',lambda p=path:p.read_bytes()),('builtins.open',lambda p=path:builtins.open(p,'rb')),('io.open',lambda p=path:io.open(p,'rb')),('os.open',lambda p=path:os.open(p,os.O_RDONLY))]
        for name,operation in methods:
            try:operation()
            except PermissionError as error:denied.append(dict(method=name,path=path.relative_to(ROOT).as_posix(),rejected=True,reason=str(error)))
            else:raise ValueError('Original input read route remained open during semantic generation')
    return denied
