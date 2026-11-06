import re
OPS={'02025ab8':('*',2),'02024e0c':('+',2),'02025ca4':('-',2),'020259b4':('s32',1),'020259e8':('u32',1)}


def arguments(text):
 result=[];start=depth=0
 for i,c in enumerate(text):
  if c in '([':depth+=1
  elif c in ')]':depth-=1
  elif c==',' and depth==0:result.append(text[start:i].strip());start=i+1
 assert depth==0;result.append(text[start:].strip());return result


def apply(text):
 start=text.index('{',text.index('u32 native_main_'));prefix,body=text[:start],text[start:];edits=[]
 def visit(value):
  match=re.search(r'\bnative_fn_('+'|'.join(OPS)+r')\(',value)
  if not match:return value
  begin=match.end();end=begin;depth=1
  while depth:
   if value[end]=='(':depth+=1
   elif value[end]==')':depth-=1
   end+=1
  args=[visit(x) for x in arguments(value[begin:end-1])];op,count=OPS[match[1]];assert len(args)==count
  replacement='(('+args[0]+') '+op+' ('+args[1]+'))' if count==2 else '(('+op+')('+args[0]+'))'
  edits.append(dict(alias=match[0][:-1],argumentCount=count,before=value[match.start():end],after=replacement,scope='known binary32 arithmetic or bounded representable cast;not arbitrary overflow/NaN equivalence'))
  return visit(value[:match.start()]+replacement+value[end:])
 return prefix+visit(body),dict(changes=edits,evidence='380/384 actual original arithmetic and compiled native chain;caller full paths/domain remain unqualified')
