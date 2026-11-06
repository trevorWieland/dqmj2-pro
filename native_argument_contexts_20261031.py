import re
from project import ROOT,read_json,sha256

PATH=ROOT/'evidence/attempts/main-native-register-abi-20261031.json'
CATALOGUE=read_json(PATH)
CONTRACTS=[x for x in CATALOGUE['results'] if x['draftContextEligible']]
assert sha256(ROOT/CATALOGUE['nativeModulePath'])==CATALOGUE['nativeModuleSha256']


def apply(context,assembly):
    used=[]
    for row in CONTRACTS:
        if row['alias'] not in assembly:continue
        pattern=r'^extern[ \t]+([^;\n]*?)[ \t]*\b'+re.escape(row['alias'])+r'\(\s*\);'
        def replace(match):
            result=f"extern {match[1].strip()} {row['alias']}({', '.join(['u32']*row['minimumArgumentWords'])});"
            used.append({'address':row['address'],'nativeBodySha256':row['nativeBodySha256'],'prototype':result,'minimumRegisterWords':row['minimumArgumentWords'],'sourceCredit':0})
            return result
        context,count=re.subn(pattern,replace,context,flags=re.M)
    return context,used
