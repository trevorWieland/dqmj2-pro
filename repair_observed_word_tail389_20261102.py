import hashlib
import re


def apply(text,assembly):
 bases=re.findall(r'^\s*add (r\d+|ip|lr), (r\d+|ip|lr), #0x470$',assembly,re.M);assert len(bases)==1
 base,owner=bases[0];loads=re.findall(r'^\s*ldr (r\d+|ip|lr), \['+base+r', (r\d+|ip|lr)\]$',assembly,re.M);stores=re.findall(r'^\s*str (r\d+|ip|lr), \['+base+r', (r\d+|ip|lr)\]$',assembly,re.M)
 assert len(loads)==len(stores)==1 and loads[0][1]==stores[0][1]
 assert '#0x477]' in assembly and '#0x10c' in assembly
 match=re.search(r'\b(?P<base>\w+) = arg0 \+ 0x470;',text);assert match;symbol=match['base'];word=re.search(r'\*\('+symbol+r' \+ (?P<index>\w+)\) = \*\('+symbol+r' \+ (?P=index)\) \+',text);assert word
 address=symbol+' + '+word['index'];before='*('+address+')';assert text.count(before)==2;text=text.replace(before,'*(u32 *)('+address+')')
 pointers=[]
 def declaration(match):
  pointers.append(dict(before=match.group(),after=match.group().replace('void','u8')));return match.group().replace('void','u8')
 lines=[]
 for line in text.splitlines(keepends=True):lines.append(line if line.startswith('#') else re.sub(r'\bvoid\s*\*',declaration,line))
 return ''.join(lines),dict(nativeWordTail=dict(baseRegister=base,ownerRegister=owner,loadRegister=loads[0][0],storeRegister=stores[0][0],indexRegister=loads[0][1],width=4),sourceWordAddress=address,explicitWordDereferences=2,opaqueByteAddressViews=pointers,scope='byte views preserve inferred opaque address arithmetic;typed word dereference follows actual LDR/STR;no aggregate extent or other helper/caller ABI claim')
