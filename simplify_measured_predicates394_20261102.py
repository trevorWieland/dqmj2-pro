import re


def apply(text):
 edits=[];pattern=r'measured_greater_(\d+) = ([^;\n]+);(?P<between>(?:\n[ \t]*(?:temp|var)_r[0-9]+(?:_[0-9]+)? = M2C_FIELD\([^;\n]+;)*)\s*\n\s*if \(measured_greater_\1\)'
 def replace(m):
  assert 'native_fn_' not in m['between'];edits.append(dict(before=m[0],predicate=m[2],between=m['between'],qualification='only local loads intervene;no call/nonlocal write;ordinary RAM/nonvolatile hypothesis'))
  return m['between']+'\n    if ('+m[2]+')'
 result=re.sub(pattern,replace,text)
 for r in edits:
  number=re.search(r'measured_greater_(\d+)',r['before'])[1];result=re.sub(r'^[ \t]*u32 measured_greater_'+number+r';\n','',result,flags=re.M)
 assert edits and 'measured_greater_' not in result
 return result,dict(changes=edits,scope='remove generated boolean materialization;preserve comparison operands and local loads;native full-caller validation pending')
