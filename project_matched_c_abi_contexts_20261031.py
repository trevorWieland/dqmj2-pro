import re
from project import ROOT,read_json,sha256,write_json,now

SCALARS={'void','u8','s8','u16','s16','u32','s32','u64','s64','f32','f64','char','short','int','long','float','double','unsigned char','signed char','unsigned short','signed short','unsigned int','signed int','unsigned long','signed long','unsigned long long','signed long long'}


def split_parameters(value):
    result=[];depth=0;begin=0
    for index,char in enumerate(value):
        depth+=char in '([';depth-=char in ')]'
        if char==',' and depth==0:result.append(value[begin:index].strip());begin=index+1
    result.append(value[begin:].strip());return result


def projected_type(value,parameter=False):
    value=re.sub(r'\b(?:const|volatile|register|restrict)\b',' ',value).strip()
    if not value or '...' in value:return None
    if re.search(r'\(\s*\*',value):return None
    if parameter:
        value=re.sub(r'\b[A-Za-z_]\w*\s*(?:\[[^]]*\])?\s*$', '',value).strip()
    if '*' in value or '[' in value:return 'void *'
    value=' '.join(value.split())
    return value if value in SCALARS else None


def catalogue():
    source_map=read_json(ROOT/'source-map.json');rows=[];rejections=[];cache={}
    for row in source_map['matchedFunctions']:
        if row['processor']!='arm9' or row['module']!='main' or row.get('program'):continue
        source=row['sourceUnit'];path=ROOT/source
        if path.suffix.lower() not in {'.c','.cpp'}:continue
        if source not in cache:cache[source]=(path.read_text(encoding='utf-8-sig'),sha256(path))
        text,digest=cache[source]
        assert digest==row['sourceSha256']
        address=int(row['address'],0);suffix=f'{address:08x}'
        pattern=r'^\s*([^;{}\n]+?)\s+(native_(?:main|fn)_'+suffix+r')\s*\(([^;{}]*)\)\s*\{'
        definitions=list(re.finditer(pattern,text,re.M))
        if len(definitions)!=1:
            rejections.append({'address':row['address'],'reason':'no unique canonical C definition','source':source});continue
        definition=definitions[0];returns=projected_type(definition[1]);raw=definition[3].strip()
        if raw=='void':parameters=[]
        elif not raw:
            rejections.append({'address':row['address'],'reason':'unspecified parameter list','source':source});continue
        else:parameters=[projected_type(x,parameter=True) for x in split_parameters(raw)]
        if returns is None or any(x is None for x in parameters):
            rejections.append({'address':row['address'],'reason':'unsupported type or callback','source':source});continue
        alias='func_'+suffix;prototype=f"extern {returns} {alias}({', '.join(parameters) if parameters else 'void'});"
        rows.append({'processor':'arm9','module':'main','program':'','mode':row['mode'],'address':row['address'],'alias':alias,'returnType':returns,'parameterTypes':parameters,'source':source,'sourceSha256':digest,'contextPrototype':prototype,'sourceCredit':0,'qualification':'Projection from the selected matching C unit; all data pointers erased to opaque ARM32 pointers; no historical signature or complete call-domain claim','callerNativeValidationRequired':True})
    return rows,rejections,source_map['buildSha256']


def main():
    rows,rejected,build=catalogue()
    output={'createdUtc':now(),'buildSha256':build,'sourceMapSha256':sha256(ROOT/'source-map.json'),'generatorSha256':sha256(ROOT/'project_matched_c_abi_contexts_20261031.py'),'sourceCredit':0,'contracts':rows,'skipped':rejected,'limitations':['New draft contexts only; no accepted source or object is changed','A selected C unit constrains an ABI hypothesis, not the original source signature or untested native domain','Callbacks, unnamed arguments, noncanonical definitions and unknown scalar typedefs are skipped','Pointer depth and pointee semantics are erased; context replacement preserves raw target pointer width only','Each new caller requires independent boundaries, defined source, genuine linking and native regression gates']}
    write_json(ROOT/'evidence/attempts/projected-matched-c-abi-contexts-20261031.json',output)
    print({'projectedContracts':len(rows),'skipped':len(rejected),'sourceCredit':0})


if __name__=='__main__':main()
