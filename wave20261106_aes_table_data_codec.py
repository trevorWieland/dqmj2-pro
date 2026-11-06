import re
import struct

KEYS={'version','kind','symbol','elementType','elementCount','finiteFieldPolynomial','affineConstant','packing','baseMixCoefficients','rotationRightBits','substitution','finalRoundReplicatedSubstitution','existingConfiguredInteriorElementViews','primarySource'}


def multiply(a,b,polynomial=0x11b):
    result=0
    for bit in range(8):
        if b&1:result^=a
        a=((a<<1)^polynomial)if a&0x80 else a<<1;b>>=1
    return result


def inverse(value,polynomial=0x11b):
    if value==0:return 0
    result=1;factor=value;exponent=254
    while exponent:
        if exponent&1:result=multiply(result,factor,polynomial)
        factor=multiply(factor,factor,polynomial);exponent>>=1
    return result


def derive(polynomial,affine,substitution,coefficients,rotation,final):
    forward=[]
    for value in range(256):
        x=inverse(value,polynomial);rotate=lambda n:((x<<n)|(x>>(8-n)))&0xff;forward.append(x^rotate(1)^rotate(2)^rotate(3)^rotate(4)^affine)
    if len(set(forward))!=256:raise ValueError('AES substitution is not a complete permutation')
    box=forward if substitution=='forward'else[forward.index(value)for value in range(256)];words=[]
    for value in box:
        word=value*0x01010101 if final else sum(multiply(value,coefficient,polynomial)<<(24-8*position)for position,coefficient in enumerate(coefficients))
        words.append(((word>>rotation)|(word<<(32-rotation)))&0xffffffff if rotation else word)
    return words


def encode(document):
    if set(document)!=KEYS or document['version']!=1 or document['kind']!='aes-rijndael-transform-table'or not re.fullmatch(r'T[ed][0-4]',document['symbol']):raise ValueError('Exact semantic AES table schema/symbol differs')
    name=document['symbol'];final=name[-1]=='4';direction='forward'if name[1]=='e'else'inverse';coefficients=[1,1,1,1]if final else[2,1,1,3]if direction=='forward'else[14,9,13,11];rotation=0 if final else int(name[-1])*8
    if(document['elementType'],document['elementCount'],document['finiteFieldPolynomial'],document['affineConstant'],document['packing'],document['substitution'],document['baseMixCoefficients'],document['rotationRightBits'],document['finalRoundReplicatedSubstitution'])!=('u32',256,'0x11b','0x63','uint32-high-coefficient-byte-first-little-endian-storage',direction,coefficients,rotation,final):raise ValueError('Exact AES word width/count/polynomial/substitution/MixColumns/rotation/packing semantics differ')
    if not isinstance(document['existingConfiguredInteriorElementViews'],list):raise ValueError('AES existing data views are not explicit metadata')
    words=derive(0x11b,0x63,direction,coefficients,rotation,final)
    return struct.pack('<256I',*words),words


def render(document,symbol):
    if not re.fullmatch(r'native_aes_T[ed][0-4]_[0-9a-f]{8}',symbol):raise ValueError('Exact ordinary C AES table symbol differs')
    payload,words=encode(document);body=['    '+', '.join(f'0x{word:08x}U'for word in words[index:index+8])+','for index in range(0,256,8)]
    return '\n'.join(['#include "aes_tables.h"',f'const AesTableWord {symbol}[256] = {{',*body,'};','']),payload


def header(assets):
    return '\n'.join(['#ifndef DQM_AES_TABLES_H','#define DQM_AES_TABLES_H','typedef unsigned int AesTableWord;','typedef char AesWordWidthMustBeFour[(sizeof(AesTableWord)==4)?1:-1];','typedef char AesWholeTableMustBe1024[(sizeof(AesTableWord[256])==1024)?1:-1];',*[f"extern const AesTableWord {row['nativeSymbol']}[256];"for row in assets],'#endif',''])
