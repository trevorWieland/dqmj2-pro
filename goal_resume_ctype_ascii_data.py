import argparse
import hashlib
import struct
from pathlib import Path
from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,configuration

SOURCE=ROOT/'src/runtime/goal_resume20261107/ctype_ascii_data'
LANE=ROOT/'evidence/lanes/parallel-wave20261107/ctype-ascii-data-source1'
WORK=ROOT/'work/goal-resume-20261107/ctype-ascii-data-source1'
AUDIT=ROOT/'evidence/lanes/parallel-wave20261107/ctype-data-frontier-source1'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_SHA='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_SHA='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
FLAGS=['-O3','-opt','speed','-proc','arm946e','-sym','on','-nolink']
TABLES=[dict(address='0x020d8d84',bytes=128,width=1,kind='upper',filename='upper.c'),dict(address='0x020d8e04',bytes=256,width=2,kind='class',filename='class_narrow.c'),dict(address='0x020d8f14',bytes=256,width=2,kind='class',filename='class_wide.c')]


def classes(c):
    alpha=65<=c<=90 or 97<=c<=122;digit=48<=c<=57;graph=33<=c<=126
    return alpha+2*(c in(9,32))+4*(c<32 or c==127)+8*digit+16*graph+32*(97<=c<=122)+64*(32<=c<=126)+128*(graph and not alpha and not digit)+256*(c in(9,10,11,12,13,32))+512*(65<=c<=90)+1024*(digit or 65<=c<=70 or 97<=c<=102)


def header():
    return r'''#ifndef DQM_ASCII_DATA_H
#define DQM_ASCII_DATA_H
enum ASCIIClass {
    ASCII_ALPHA=1, ASCII_BLANK=2, ASCII_CONTROL=4, ASCII_DIGIT=8,
    ASCII_GRAPH=16, ASCII_LOWER=32, ASCII_PRINT=64, ASCII_PUNCT=128,
    ASCII_SPACE=256, ASCII_UPPER=512, ASCII_HEX=1024
};
#define ASCII_BETWEEN(c,a,b) ((c)>=(a)&&(c)<=(b))
#define ASCII_IS_UPPER(c) ASCII_BETWEEN(c,'A','Z')
#define ASCII_IS_LOWER(c) ASCII_BETWEEN(c,'a','z')
#define ASCII_IS_ALPHA(c) (ASCII_IS_UPPER(c)||ASCII_IS_LOWER(c))
#define ASCII_IS_DIGIT(c) ASCII_BETWEEN(c,'0','9')
#define ASCII_IS_GRAPH(c) ASCII_BETWEEN(c,'!','~')
#define ASCII_IS_SPACE(c) ((c)==' '||ASCII_BETWEEN(c,9,13))
#define ASCII_TO_UPPER(c) (ASCII_IS_LOWER(c)?(c)-'a'+'A':(c))
#define ASCII_CLASS(c) (\
    (ASCII_IS_ALPHA(c)?ASCII_ALPHA:0)|\
    ((c)==9||(c)==' '?ASCII_BLANK:0)|\
    ((c)<32||(c)==127?ASCII_CONTROL:0)|\
    (ASCII_IS_DIGIT(c)?ASCII_DIGIT:0)|\
    (ASCII_IS_GRAPH(c)?ASCII_GRAPH:0)|\
    (ASCII_IS_LOWER(c)?ASCII_LOWER:0)|\
    (ASCII_BETWEEN(c,' ','~')?ASCII_PRINT:0)|\
    (ASCII_IS_GRAPH(c)&&!ASCII_IS_ALPHA(c)&&!ASCII_IS_DIGIT(c)?ASCII_PUNCT:0)|\
    (ASCII_IS_SPACE(c)?ASCII_SPACE:0)|\
    (ASCII_IS_UPPER(c)?ASCII_UPPER:0)|\
    (ASCII_IS_DIGIT(c)||ASCII_BETWEEN(c,'A','F')||ASCII_BETWEEN(c,'a','f')?ASCII_HEX:0))
typedef char ASCIIByteWidth[sizeof(unsigned char)==1?1:-1];
typedef char ASCIIClassWidth[sizeof(unsigned short)==2?1:-1];
typedef char ASCIIExecutionSet['A'==65&&'a'==97&&'0'==48&&'~'==126?1:-1];
#endif
'''


def render(row):
    if row not in TABLES:raise ValueError('Unreviewed ASCII storage definition')
    macro='ASCII_TO_UPPER'if row['kind']=='upper'else'ASCII_CLASS';ctype='unsigned char'if row['width']==1 else'unsigned short';name='native_data_'+f'{int(row["address"],0):08x}'
    lines=[header(),f'const {ctype} {name}[128] = {{']
    lines.extend('    '+', '.join(macro+'('+str(c)+')'for c in range(start,start+8))+(','if start<120 else'')for start in range(0,128,8))
    text='\n'.join(lines+['};','']);values=[c-32 if 97<=c<=122 else c for c in range(128)]if row['kind']=='upper'else[classes(c)for c in range(128)]
    payload=bytes(values)if row['width']==1 else struct.pack('<128H',*values)
    return text,payload


def guarded_render():
    original=Path.open;blocked=[]
    def open_source(path,*args,**kwargs):
        if any(path.resolve().is_relative_to(ROOT/prefix)for prefix in['inputs','extract','deps/reference']):raise PermissionError('Original inputs are unavailable during independent ASCII generation')
        return original(path,*args,**kwargs)
    with patch.object(Path,'open',open_source):
        outputs=[(row,*render(row))for row in TABLES];common=header()
        for path in[ROOT/'extract/arm9/arm9.bin',configuration()['rom']]:
            try:path.read_bytes()
            except PermissionError:blocked.append(str(path.relative_to(ROOT)))
            else:raise ValueError('Original input generation guard did not reject a read')
    return common,outputs,blocked


def create():
    if SOURCE.exists()or LANE.exists()or WORK.exists():raise ValueError('Admitted implementation roots must be new')
    if sha256(AUDIT/'proposal.json')!='5934648214341b4fb103e3deb812fe0fd17628b50ae4fcb4d2f64bcc84be8382'or sha256(AUDIT/'seal.json')!='6cd5ff47a3ca6ebac86f1d6c128725cc3d2e701863f5f4c87191e9622a25d81b':raise ValueError('Reviewed frontier changed')
    for pin in read_json(AUDIT/'seal.json')['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen frontier input changed')
    if sha256(COMPILER)!=COMPILER_SHA or sha256(LINKER)!=LINKER_SHA:raise ValueError('Established data toolchain differs')
    approved=read_json(AUDIT/'audit.json')['tables'];claim=[]
    for row in TABLES:
        original=next(r for r in approved if int(r['address'],0)==int(row['address'],0));claim.append(dict(row,program='',processor='arm9',module='main',mode='data',section='.rodata',targetSha256=original['targetSha256'],source=(SOURCE/row['filename']).relative_to(ROOT).as_posix(),id=configuration()['romSha256']+'/arm9/main/rodata/'+f'{int(row["address"],0):08x}'))
    LANE.mkdir(parents=True)
    write_json(LANE/'claim.json',dict(schemaVersion=1,status='coordinator-admitted-bounded-ASCII-data',sourceCredit=0,claimedStorage=claim,initializedBytes=640,functions=0,executableBytes=0,zeroFillBytes=0,paddingBytes=0,encodedAssetBytes=0,sourceRoot=SOURCE.relative_to(ROOT).as_posix(),workRoot=WORK.relative_to(ROOT).as_posix(),frontier=dict(path=(AUDIT/'seal.json').relative_to(ROOT).as_posix(),sha256=sha256(AUDIT/'seal.json')),compilerRecipe=dict(compiler=COMPILER.relative_to(ROOT).as_posix(),sha256=COMPILER_SHA,flags=FLAGS,establishedPrecedent='match_main_ascii_lower_data_20261031.py'),rule='Three distinct bounded typed views only. No original declaration alignment or enclosing object-size claim; no other data/function scope or shared adoption.'))
    common,outputs,blocked=guarded_render();SOURCE.mkdir(parents=True);(SOURCE/'ascii.h').write_text(common)
    for row,text,payload in outputs:(SOURCE/row['filename']).write_text(text)
    write_json(LANE/'source-generation.json',dict(status='independent-semantic-ASCII-source-created',sourceCredit=0,blockedOriginalReads=blocked,files=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p))for p in sorted(SOURCE.iterdir())],independentAlgorithm='Explicit ASCII range/category predicates for integer domain0..127; C initializers contain predicate applications to indices, not target-byte literals.',distinctClassSymbols=True))
    print(dict(claim=(LANE/'claim.json').relative_to(ROOT).as_posix(),objects=3,initializedBytes=640,sourceCredit=0),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--create',action='store_true',required=True);parser.parse_args();create()
