import gzip
import hashlib
import json
import struct
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
import ov001_selector917_machine_20261102 as M
import ov001_selector917_model_20261102 as G


def compact(result):
    return {k:v for k,v in result.items()if k!='memory'}|dict(completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    mainInfo,main,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov001')
    traces=[]
    totals=dict(firstDispatcherTopReturns=0,secondDispatcherTopReturns=0,getterTopReturns=0,actualTopReturns=0,actualNestedPhysicalReturns=0,suppliedNotifications=0,selector13=0,selector14=0)
    for p in G.profiles()[:64]:
        vm=M.Machine(main,overlay,None,p)
        initial=bytearray(vm.beforeState)
        first=vm.run(M.ENTRY)
        seed=(p['seed']*0x41C64E6D+0x3039)&0xFFFFFFFF
        draw=(seed>>16)%1000
        selector=13 if draw<p['threshold']else 14
        expected=bytearray(initial)
        expected[0xA]=selector
        expected[0xF]=0
        firstWrites=[[M.RNG,4,seed],[M.STATE+0xA,1,selector],[M.STATE+0xF,1,0]]
        if first['registers'][0]!=0 or first['stateHex']!=expected.hex()or first['rngState']!=seed or first['writes']!=firstWrites:
            raise ValueError(('920 first dispatcher effects',p['ordinal']))
        if [r['entry']for r in first['nativeEntries']]!=[hex(M.SELECTOR),'0x205fd60','0x203d294','0x2026350']:
            raise ValueError('920 actual first dispatch chain differs')
        if [r['entry']for r in first['nativePhysicalReturns']]!=['0x205fd60','0x2026350','0x203d294',hex(M.SELECTOR)]:
            raise ValueError('920 actual first physical returns differ')
        if G.logical_providers(first)!=[dict(target=hex(M.NOTICE),consumedWords=[0,1],returnWord=0xC0DEC0DE)]:
            raise ValueError('920 notification contract differs')
        totals['selector13'if selector==13 else'selector14']+=1
        totals['firstDispatcherTopReturns']+=1
        totals['actualTopReturns']+=1
        totals['actualNestedPhysicalReturns']+=len(first['nativePhysicalReturns'])
        totals['suppliedNotifications']+=len(first['provided'])
        second=None
        secondDraw=None
        if selector==14:
            second=vm.run(M.ENTRY)
            seed=(seed*0x41C64E6D+0x3039)&0xFFFFFFFF
            secondDraw=(seed>>16)%256
            expected[0x1A]=40 if secondDraw<128 else 50
            secondWrites=[[M.RNG,4,seed],[M.STATE+0x1A,1,expected[0x1A]]]
            if second['registers'][0]!=0 or second['rngState']!=seed or second['stateHex']!=expected.hex()or second['writes']!=secondWrites:
                raise ValueError(('920 second dispatcher effects',p['ordinal']))
            if [r['entry']for r in second['nativeEntries']]!=[hex(M.CHILD),'0x203d294','0x2026350']:
                raise ValueError('920 actual second dispatcher chain differs')
            if [r['entry']for r in second['nativePhysicalReturns']]!=['0x2026350','0x203d294',hex(M.CHILD)]:
                raise ValueError('920 actual second return chain differs')
            if second['provided']:raise ValueError('920 second dispatcher unexpectedly provided')
            totals['secondDispatcherTopReturns']+=1
            totals['actualTopReturns']+=1
            totals['actualNestedPhysicalReturns']+=len(second['nativePhysicalReturns'])
        getter=vm.run(M.GETTER)
        if getter['registers'][0]!=(M.SCRATCH if p['gate']else 0)or getter['stateHex']!=expected.hex()or getter['rngState']!=seed or getter['writes']:
            raise ValueError('920 driver getter model differs')
        totals['getterTopReturns']+=1
        totals['actualTopReturns']+=1
        traces.append(dict(profile=p,first=compact(first),second=compact(second)if second else None,getter=compact(getter),firstDraw=draw,secondDraw=secondDraw,observedSelector=selector,allPassed=True))
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-selector920-chain-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],totals=totals,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Actual original dispatcher021FBD6C enters actual021FAFEC under supplied selector12/subphase0x6E; wait word0. Original RNG(1000) writes selector13 for signed result<signed16 threshold,14 otherwise. No source substitutions or instruction patching.','For35 selector14 outcomes, the test driver invokes the same actual dispatcher again on the unchanged resulting VM state. Child phase+0x1A was supplied as30 before the first call and retained, so actual021FB960 immediately draws RNG(256). No manual memory edits occur between calls.','This demonstrates actual parent/child code ordering under explicit synthetic fields. It does NOT establish that ordinary scene phase30 is reached this way or that these draws are adjacent in a game: omitted child phases/services may consume RNG before30. Selector13 branch is not advanced into its unsupported next handler.','Original wait getter, RNG and division execute; only notification021E3544(0,1) is supplied without memory effects and with legal caller-saved/NZCV clobbers. Busy word, score, selector/subphase, child phase, seed and getter-gate byte are provided input state.','The subsequent getter021FBE70 is explicitly invoked by the test driver, not by the dispatcher. It only tests the supplied raw u8 scratch+0x67 and establishes no complete-record, scene-validity, initialization, persistence or game-role meaning.','Top returns163 and nested physical returns361 are separate actual counts; no double counting. This is zero-credit original-native semantic evidence, no exact/module/ROM source or host/device claim.'])
    write_json(ROOT/'evidence/application/ov001-selector920-native-chain-20261102.json',report)
    print(totals,flush=True)

if __name__=='__main__':execute()
