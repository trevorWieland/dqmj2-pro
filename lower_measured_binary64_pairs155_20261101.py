import re
from qualified_float_chain153_context_20261101 import catalogue


def lower(text):
    catalogue()
    receipts=[]
    def replace_multiply(match):
        name=match[1]
        assert re.search(r'\bf64\s+'+re.escape(name)+r'\s*;',text),('MissingBinary64Temporary',name)
        replacement='func_02024540(1.5, '+name+')'
        receipts.append(dict(kind='multiply',input=match[0],output=replacement,temporary=name,
            constantWords=[0,0x3FF80000]))
        return replacement
    def replace_truncate(match):
        name=match[1]
        assert re.search(r'\bf64\s+'+re.escape(name)+r'\s*;',text),('MissingBinary64Temporary',name)
        replacement='func_02024394('+name+')'
        receipts.append(dict(kind='truncate',input=match[0],output=replacement,temporary=name))
        return replacement
    text=re.sub(r'func_02024540\(0, 0x3FF80000, M2C_BITWISE\(s32, (temp_ret(?:_\d+)?)\), SECOND_REG\(\1\)\)',replace_multiply,text)
    text=re.sub(r'func_02024394\(M2C_BITWISE\(s32, (temp_ret(?:_\d+)?)\), SECOND_REG\(\1\)\)',replace_truncate,text)
    return text,receipts
