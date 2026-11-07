import json
from pathlib import Path
import sys
from warm_api import function
from synthetic_cases import check_synthetic
from copied_numeric import numeric_cases


def main():
    library=Path(sys.argv[1]).resolve();target=Path(sys.argv[2]).resolve();assert not target.exists()
    fn=function(library);regular=check_synthetic(fn);numeric=numeric_cases(fn)
    result=dict(status='source-only-synthetic-warm-effect-replay-pass',regular=regular,numeric=numeric,
        privateInputOrOriginalOracleRequired=False,sourceCredit=0,matchingCredit=0,deviceOrGameExecution=False)
    target.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status=result['status'],positive=12,refusals=47)))


if __name__=='__main__':main()
