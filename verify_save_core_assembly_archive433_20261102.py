import gzip
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(raw):return hashlib.sha256(raw).hexdigest()
def main():
 r=json.loads((ROOT/'evidence/verification/save-core-analysis-assembly433-20261102.json').read_text());p=ROOT/r['sidecar']['path'];packed=p.read_bytes();raw=gzip.decompress(packed);assert sha(packed)==r['sidecar']['sha256'] and sha(raw)==r['sidecar']['contentSha256'];rows=json.loads(raw);assert len(rows)==104
 for x in rows:
  data=x['text'].encode('utf-8');assert sha(data)==x['rawSha256'];normalized=x['text'].replace('\r\n','\n').replace('\r','\n').encode('utf-8');assert sha(normalized)==x['normalizedLfSha256']
  if x['recordedAnalysisSha256']:assert sha(normalized)==x['recordedAnalysisSha256']
 assert sum(x['path'].endswith('input.s') for x in rows)==52;print(json.dumps(dict(records=104,assemblies=52,sourceCredit=0,functionReturns=0,sidecarSha256=sha(packed))))
if __name__=='__main__':main()
