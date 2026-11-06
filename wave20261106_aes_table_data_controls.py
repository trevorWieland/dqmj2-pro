import copy
import struct
from project import ROOT,read_json
from wave20261106_aes_table_data_paths import SOURCE
from wave20261106_aes_table_data_codec import encode,derive
from wave20261106_aes_table_data_build import compile_link,inspect_object
from wave20261106_aes_table_data_validate import validate_layout,validate_primary,validate_native,validate_views


def rejected(call):
    try:call()
    except(ValueError,AssertionError,KeyError,StopIteration):return True
    raise ValueError('Wrong AES semantic/C/object/native/namespace/element-view input admitted')


def c_source(symbol,words):
    return '\n'.join(['#include "aes_tables.h"',f'const AesTableWord {symbol}[{len(words)}] = {{',*['    '+', '.join(f'0x{x:08x}U'for x in words[i:i+8])+','for i in range(0,len(words),8)],'};',''])


def execute(layout,image,directory):
    schema=[];scope=[];views=[]
    for row in layout['assets']:
        doc=read_json(ROOT/row['semanticSource'])
        for field,value in [('finiteFieldPolynomial','0x11d'),('affineConstant','0x62'),('rotationRightBits',(doc['rotationRightBits']+8)%32),('elementCount',255),('packing','big-endian')]:
            wrong=dict(doc);wrong[field]=value;schema.append(dict(table=doc['symbol'],case=field,rejected=rejected(lambda wrong=wrong:encode(wrong))))
        for index,view in enumerate(doc['existingConfiguredInteriorElementViews']):
            payload,_=encode(doc)
            for field,value in [('byteOffset',view['byteOffset']+4),('elementIndex',view['elementIndex']+1),('actualOriginalMainReferences',[]),('sameAddressOtherOverlayConfiguredRecords',[])]:
                wrong=copy.deepcopy(doc);wrong['existingConfiguredInteriorElementViews'][index][field]=value;views.append(dict(alias=view['nativeAlias'],case=field,rejected=rejected(lambda wrong=wrong:validate_views(row,wrong,payload,image))))
            wrong=copy.deepcopy(doc);wrong['existingConfiguredInteriorElementViews'][index]['actualOriginalMainReferences'][0]['originalModuleExpression']='overlay(6)';views.append(dict(alias=view['nativeAlias'],case='plural-main-namespace-rebound',rejected=rejected(lambda wrong=wrong:validate_views(row,wrong,payload,image))))
    for field,value in [('program','foreign'),('processor','arm7'),('module','ov000'),('kind','function'),('mode','thumb'),('address','0x22088bc'),('elementCount',255),('elementType','u16')]:
        wrong=copy.deepcopy(layout);wrong['assets'][0][field]=value;scope.append(dict(case=field,rejected=rejected(lambda wrong=wrong:validate_layout(wrong))))
    row=next(r for r in layout['assets']if r['primarySymbol']=='Te0');doc=read_json(ROOT/row['semanticSource']);payload,words=encode(doc);wrong_doc=copy.deepcopy(doc);wrong_doc['primarySource']['sha256']='0'*64;primary=rejected(lambda:validate_primary(wrong_doc,payload));changed=bytearray(image);changed[int(row['address'],0)-0x21d7240]^=1;native=rejected(lambda:validate_native(row,payload,bytes(changed)));whole=[]
    cases=[('polynomial',derive(0x11d,0x63,'forward',[2,1,1,3],0,False)),('affine',derive(0x11b,0x62,'forward',[2,1,1,3],0,False)),('substitution',derive(0x11b,0x63,'inverse',[2,1,1,3],0,False)),('rotation',derive(0x11b,0x63,'forward',[2,1,1,3],8,False)),('packing',[int.from_bytes(x.to_bytes(4,'little'),'big')for x in words]),('coefficients',derive(0x11b,0x63,'forward',[3,1,1,2],0,False)),('extent255',words[:255]),('extent257',words+[0])]
    for label,wrong_words in cases:
        folder=directory/label;folder.mkdir(parents=True,exist_ok=True);header=(SOURCE/'aes_tables.h').read_text();header=header.replace(f"{row['nativeSymbol']}[256]",f"{row['nativeSymbol']}[{len(wrong_words)}]");(folder/'aes_tables.h').write_text(header,encoding='utf-8');source=folder/'wrong.c';source.write_text(c_source(row['nativeSymbol'],wrong_words),encoding='utf-8');wrong_payload=struct.pack('<'+'I'*len(wrong_words),*wrong_words);proof=compile_link(row,source,wrong_payload,folder/'proof')
        whole.append(dict(case=label,genuinelyCompiledAndLinked=True,wrongCompleteTypedObjectOrPayloadRejected=rejected(lambda:inspect_object(ROOT/proof['object'],row['nativeSymbol'],payload)),wrongNativeMathPackingOrExtentRejected=rejected(lambda:validate_native(row,wrong_payload,image)),object=proof['object'],objectSha256=proof['objectSha256'],realLink=proof['realLink']))
    folder=directory/'width16';folder.mkdir(parents=True,exist_ok=True);(folder/'aes_tables.h').write_text((SOURCE/'aes_tables.h').read_text().replace('typedef unsigned int AesTableWord;','typedef unsigned short AesTableWord;'),encoding='utf-8');source=folder/'wrong.c';source.write_text(c_source(row['nativeSymbol'],words),encoding='utf-8');width=rejected(lambda:compile_link(row,source,payload,folder/'proof'))
    return dict(passed=True,semanticSchemaControls=schema,namespaceTypeExtentControls=scope,threeInteriorElementViewControls=views,changedPrimarySourceRejected=primary,changedFullNativeOverlayRejected=native,genuineWrongCObjects=whole,genuineWrongCCount=len(whole),actualWrongWidthHeaderCompileRejected=width,actualFunctionOrProviderOrNetworkOrDeviceExecutions=0,additionalAliasOrGapOrBssCredit=0)
