import re
from lower_measured_binary32_flags388_20261102 import arguments,SYMBOLS


def macro(expression):
 expression=expression.strip()
 if not expression.startswith('M2C_BITWISE(') or not expression.endswith(')'):return None
 args=arguments(expression[12:-1]);return args if len(args)==2 else None


def scalar_kind(expression,variables):
 expression=expression.strip()
 if expression in variables:return variables[expression]
 if expression.startswith('M2C_FIELD('):return arguments(expression[10:-1])[1].replace('*','').strip()
 m=re.match(r'func_([0-9a-f]{8})\(',expression)
 if m:return SYMBOLS.get(int(m[1],16),('u32',''))[0]
 item=macro(expression)
 if item:return item[0]
 return 'unknown'


def promote(raw):
 variables={name:kind for kind,name in re.findall(r'\b(f32|s32|u32)\s+([A-Za-z_]\w*)\s*;',raw)};promoted=[]
 for name,kind in list(variables.items()):
  if kind not in ('s32','u32'):continue
  writes=list(re.finditer(r'\b'+re.escape(name)+r' = ([^;\n]+);',raw))
  if not writes:continue
  all_float=True;replacement=[]
  for m in writes:
   expression=m[1].strip();item=macro(expression)
   if item and item[0] in ('s32','u32') and scalar_kind(item[1],variables)=='f32':replacement.append((m[0],name+' = '+item[1]+';'))
   elif expression.startswith('M2C_FIELD('):
    args=arguments(expression[10:-1])
    if args[1].replace('*','').strip() not in ('s32','u32'):all_float=False;break
    args[1]='f32 *';replacement.append((m[0],name+' = M2C_FIELD('+', '.join(args)+');'))
   else:all_float=False;break
  if not all_float:continue
  rest=re.sub(r'\b'+kind+r'\s+'+name+r'\s*;','',raw);rest=re.sub(r'\b'+name+r'(?= = )','LHS',rest);rest=re.sub(r'M2C_BITWISE\(f32, '+name+r'\)','FLOAT_READ',rest)
  if re.search(r'\b'+name+r'\b',rest):continue
  before=raw;raw=re.sub(r'\b'+kind+r'\s+'+name+r'\s*;','f32 '+name+';',raw)
  for old,new in replacement:raw=raw.replace(old,new)
  variables[name]='f32';promoted.append(dict(variable=name,before=kind,after='f32',assignments=[dict(before=a,after=b) for a,b in replacement],qualification='all uses explicitly reinterpret as binary32;all writes32-bit field load or known f32 helper result'))
 return raw,dict(promotions=promoted,scope='carrier-only dataflow review;ordinary integer uses disqualify promotion')


def simplify(raw):
 variables={name:kind for kind,name in re.findall(r'\b(f32|s32|u32)\s+([A-Za-z_]\w*)\s*;',raw)};edits=[]
 def visit(text):
  token='M2C_BITWISE(';at=text.find(token)
  if at<0:return text
  begin=at+len(token);end=begin;depth=1
  while depth:
   if text[end]=='(':depth+=1
   elif text[end]==')':depth-=1
   end+=1
  target,expression=arguments(text[begin:end-1]);inner=macro(expression);replacement=None
  if target=='f32' and inner and inner[0] in ('s32','u32') and scalar_kind(inner[1],variables)=='f32':replacement=visit(inner[1])
  else:
   expression=visit(expression)
   if target==scalar_kind(expression,variables):replacement=expression
  if replacement is None:replacement='M2C_BITWISE('+target+', '+expression+')'
  before=text[at:end]
  if before!=replacement:edits.append(dict(before=before,after=replacement))
  return text[:at]+replacement+visit(text[end:])
 return visit(raw),dict(changes=edits,scope='identical32-bit representation round trips only;no numeric casts invented')
