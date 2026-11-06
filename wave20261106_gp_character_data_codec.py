import re

KIND='whole-primary-c-character-object'


def literal(expression):
    if not isinstance(expression,str):raise ValueError('Character initializer must be a real C string literal expression')
    token=re.compile(r'"(?:\\[\s\S]|[^"\\])*"');parts=[];out=bytearray();cursor=0;simple={'a':7,'b':8,'f':12,'n':10,'r':13,'t':9,'v':11,'\\':92,'"':34,"'":39,'?':63}
    for match in token.finditer(expression):
        if expression[cursor:match.start()].strip():raise ValueError('Character initializer includes nonliteral C tokens')
        parts.append(match.group());cursor=match.end();body=match.group()[1:-1];i=0
        while i<len(body):
            c=body[i];i+=1
            if c!='\\':
                if c in '\r\n'or ord(c)>127:raise ValueError('Invalid narrow ASCII C literal')
                out.append(ord(c));continue
            if i==len(body):raise ValueError('Truncated C character escape')
            c=body[i];i+=1
            if c in simple:out.append(simple[c])
            elif c in '01234567':
                digits=c
                while i<len(body)and len(digits)<3 and body[i]in'01234567':digits+=body[i];i+=1
                n=int(digits,8)
                if n>255:raise ValueError('Out-of-byte C octal escape')
                out.append(n)
            elif c=='x':
                first=i
                while i<len(body)and body[i]in'0123456789abcdefABCDEF':i+=1
                if first==i or int(body[first:i],16)>255:raise ValueError('Invalid C hex character escape')
                out.append(int(body[first:i],16))
            else:raise ValueError('Unsupported or continued C literal escape')
    if not parts or expression[cursor:].strip():raise ValueError('Incomplete C character literal expression')
    return bytes(out),' '.join(parts)


def encode(document):
    if set(document)!={'version','kind','characterValue','literalExpression','includesFinalNul','bytes','primaryReference'}or document['version']!=1 or document['kind']!=KIND or document['includesFinalNul']is not True:raise ValueError('Exact whole-character source schema differs')
    text=document['characterValue']
    if not isinstance(text,str)or not text or any(ord(c)==0 or ord(c)>126 or ord(c)<32 and c not in '\t\r\n'for c in text):raise ValueError('Whole narrow character meaning is invalid')
    raw,expression=literal(document['literalExpression'])
    if raw!=text.encode('ascii')or document['bytes']!=len(raw)+1:raise ValueError('Whole primary C expression/character value/terminator extent differs')
    return raw+b'\0',expression


def render(document,symbol):
    if not re.fullmatch(r'native_gp_character_[0-9a-f]{8}',symbol):raise ValueError('Exact typed GP character object symbol differs')
    payload,expression=encode(document)
    return '#include "characters.h"\nconst char '+symbol+'[] = '+expression+';\n',payload
