import copy
import json
from project import ROOT,read_json,sha256
from wave20261106_auth_character_data_codec import encode
from wave20261106_auth_character_data_paths import SOURCE
from wave20261106_auth_character_data_build import compile_link,inspect_object
from wave20261106_auth_character_data_validate import validate_layout,validate_reference,validate_native


def rejected(call):
    try:call()
    except(ValueError,AssertionError,KeyError):return True
    raise ValueError('Wrong Auth character source/native/scope admitted')


def execute(layout,image,directory):
    schema=[]
    for row in layout['assets']:
        document=read_json(ROOT/row['semanticSource']);wrong='!'+document['characterValue'][1:]
        if wrong==document['characterValue']:wrong='?'+wrong[1:]
        for label,value in [('character',dict(document,characterValue=wrong)),('NUL',dict(document,includesFinalNul=False)),('extent',dict(document,bytes=document['bytes']+1))]:schema.append(dict(address=row['address'],case=label,rejected=rejected(lambda value=value:encode(value))))
    scope=[]
    for field,value in [('program','foreign'),('processor','arm7'),('module','ov000'),('kind','function'),('mode','arm'),('address','0x20deb48')]:
        wrong=copy.deepcopy(layout);wrong['assets'][0][field]=value;scope.append(dict(case=field,rejected=rejected(lambda wrong=wrong:validate_layout(wrong))))
    first=layout['assets'][0];doc=read_json(ROOT/first['semanticSource']);wrong=copy.deepcopy(doc);wrong['primaryReference']['sha256']='0'*64;primary=rejected(lambda:validate_reference(wrong));changed=bytearray(image);changed[int(first['address'],0)-0x2000000]^=1;payload,_=encode(doc);native=rejected(lambda:validate_native(first,payload,bytes(changed)));whole=[]
    selected=[first,next(row for row in layout['assets']if'\\'in read_json(ROOT/row['semanticSource'])['literalExpression'])]
    for row in selected:
        doc=read_json(ROOT/row['semanticSource']);payload,_=encode(doc);name=row['nativeSymbol'];n=len(payload)
        for label in ['character','NUL','extent']:
            folder=directory/f"{int(row['address'],0):08x}"/('terminator'if label=='NUL'else label);folder.mkdir(parents=True,exist_ok=True);text=(SOURCE/'characters.h').read_text();declaration='[]'
            if label=='character':
                value=chr(ord(doc['characterValue'][0])^1)+doc['characterValue'][1:];expression=json.dumps(value);wrong_payload=value.encode('ascii')+b'\0'
            elif label=='NUL':expression=doc['literalExpression']+' "\\001"';declaration=f'[{n}]';wrong_payload=payload[:-1]+b'\1'
            else:expression=doc['literalExpression'];declaration=f'[{n+1}]';wrong_payload=payload+b'\0';text=text.replace(f'{name}[{n}]',f'{name}[{n+1}]')
            (folder/'characters.h').write_text(text,encoding='utf-8');source=folder/'wrong.c';source.write_text('#include "characters.h"\nconst char '+name+declaration+' = '+expression+';\n',encoding='utf-8');proof=compile_link(row,source,wrong_payload,folder/'proof')
            whole.append(dict(address=row['address'],case=label,genuineWrongCCompilationAndLink=True,wrongCompleteObjectRejected=rejected(lambda:inspect_object(ROOT/proof['object'],name,payload)),wrongNativeMeaningNulOrExtentRejected=rejected(lambda:validate_native(row,wrong_payload,image)),object=proof['object'],objectSha256=proof['objectSha256'],realLink=proof['realLink']))
    return dict(passed=True,wholeWrongCControls=len(whole),genuinelyLinkedWrongCObjects=whole,schemaControls=schema,namespaceControls=scope,changedPrimarySourceRejected=primary,changedFullNativeImageRejected=native,actualFunctionOrNetworkOrDeviceExecutions=0)
