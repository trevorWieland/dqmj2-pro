import copy
import json
import shutil
from project import ROOT,read_json,write_json
from wave20261106_gp_character_data_paths import SOURCE,EVIDENCE,WORK,assert_owned
from wave20261106_gp_character_data_codec import encode
from wave20261106_gp_character_data_build import compile_link,inspect_object
from wave20261106_gp_character_data_validate import validate_layout,validate_native,validate_reference


def rejected(call):
    try:call()
    except (ValueError,AssertionError,KeyError):return True
    raise ValueError('Meaningful wrong GP character input admitted')


def execute(layout,claim,image):
    assert_owned();schema=[]
    for row in layout['assets']:
        document=read_json(ROOT/row['semanticSource']);changes=[('character',dict(document,characterValue='!'+document['characterValue'][1:])),('missing-NUL',dict(document,includesFinalNul=False)),('extent',dict(document,bytes=document['bytes']+1))]
        if changes[0][1]['characterValue']==document['characterValue']:changes[0]=('character',dict(document,characterValue='?'+document['characterValue'][1:]))
        for label,wrong in changes:schema.append(dict(address=row['address'],case=label,rejected=rejected(lambda:encode(wrong))))
    namespace=[]
    for field,value in [('program','foreign'),('processor','arm7'),('module','ov000'),('mode','arm'),('kind','function'),('address',hex(int(layout['assets'][0]['address'],0)+4))]:
        wrong=copy.deepcopy(layout);wrong['assets'][0][field]=value;namespace.append(dict(case=field,rejected=rejected(lambda:validate_layout(wrong,claim))))
    document=read_json(ROOT/layout['assets'][0]['semanticSource']);wrong=copy.deepcopy(document);wrong['primaryReference']['sha256']='0'*64;reference=rejected(lambda:validate_reference(wrong));changed=bytearray(image);changed[int(layout['assets'][0]['address'],0)-0x2000000]^=1;payload,_=encode(document);native=rejected(lambda:validate_native(layout['assets'][0],payload,bytes(changed)));whole=[]
    for row in [layout['assets'][0],next(x for x in layout['assets']if'\\'in read_json(ROOT/x['semanticSource'])['characterValue'])]:
        document=read_json(ROOT/row['semanticSource']);payload,_=encode(document);name=row['nativeSymbol']
        for label in ['character','NUL','extent']:
            folder=WORK/'wrong-c'/row['address']/('terminator'if label=='NUL'else label);folder.mkdir(parents=True,exist_ok=True);header=(SOURCE/'characters.h').read_text();n=len(payload)
            if label=='character':
                text=chr(ord(document['characterValue'][0])^1)+document['characterValue'][1:];literal=json.dumps(text);wrong_payload=text.encode('ascii')+b'\0';declaration='[]'
            elif label=='NUL':literal=document['literalExpression']+' "\\001"';wrong_payload=payload[:-1]+b'\1';declaration=f'[{n}]'
            else:
                literal=document['literalExpression'];wrong_payload=payload+b'\0';declaration=f'[{n+1}]';header=header.replace(f'{name}[{n}]',f'{name}[{n+1}]')
            (folder/'characters.h').write_text(header);source=folder/'wrong.c';source.write_text('#include "characters.h"\nconst char '+name+declaration+' = '+literal+';\n');proof=compile_link(row,source,wrong_payload,folder/'proof');deny=rejected(lambda:validate_native(row,wrong_payload,image));object_deny=rejected(lambda:inspect_object(ROOT/proof['object'],name,payload));whole.append(dict(address=row['address'],case=label,actualCompiledBytes=len(wrong_payload),genuineCAndMwLink=True,compiledWrongWholeObjectRejected=object_deny,nativeMeaningOrNulOrExtentRejected=deny,object=proof['object'],objectSha256=proof['objectSha256'],realLink=proof['realLink']))
    result=dict(passed=True,schemaControls=schema,namespaceControls=namespace,changedPrimarySourceRejected=reference,changedFullNativeImageRejected=native,genuinelyLinkedWrongCObjects=whole,wholeWrongCControls=len(whole),functionOrDeviceExecutions=0,ordinaryFunctionCredit=0,alignmentCredit=0)
    write_json(EVIDENCE/'controls.json',result);return result
