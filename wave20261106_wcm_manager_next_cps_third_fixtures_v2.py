from project import ROOT
import wave20261106_wcm_manager_next_cps_third_fixtures as F

def prove(row,native,source):
 result=F.prove(row,native,source)
 if int(row['address'],0)!=0x208c998:return result
 image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[]
 for kind,target in [(0,'0x208c8d0'),(8,'0x208c848')]:
  vector=next(v for v in F.F.cases(0x208c998)if v['valid']and v['ipvalid']and v['type']==kind)
  original=F.run(image,row,native,vector,37+kind);rebuilt=F.run(image,row,source,vector,37+kind)
  if original!=rebuilt or not original['modelPassed']or [call[0]for call in original['calls']]!=['0x208bb98','0x208c97c',target]:raise ValueError('Intended native/source ICMP dispatch branch was not reached')
  records.append(dict(type=kind,expectedHandler=target,actualNativeAndSourceHandlerReached=True,nativeCalls=original['calls'],sourceCalls=rebuilt['calls'],traceSha256=original['traceSha256']))
 result.update(intendedIcmpDispatchBranchesReached=records,intendedIcmpDispatchBranchReachRequired=True,actualNativeAndSourceCallerReturns=result['actualNativeAndSourceCallerReturns']+4)
 return result
