import ast
from pathlib import Path


def required_json_reads(tree,root):
    environment={'ROOT':root}
    def value(node):
        if isinstance(node,ast.Constant) and isinstance(node.value,str):return node.value
        if isinstance(node,ast.Name):return environment.get(node.id)
        if isinstance(node,ast.BinOp):
            left,right=value(node.left),value(node.right)
            if left is None or right is None:return None
            if isinstance(node.op,ast.Div) and isinstance(right,str):return Path(left)/right
            if isinstance(node.op,ast.Add) and isinstance(left,str) and isinstance(right,str):return left+right
        if isinstance(node,ast.Attribute) and node.attr=='parent':
            item=value(node.value)
            if isinstance(item,Path):return item.parent
        if isinstance(node,ast.Call):
            if isinstance(node.func,ast.Name) and node.func.id=='Path' and len(node.args)==1:
                item=value(node.args[0])
                if isinstance(item,str):return Path(item)
            if isinstance(node.func,ast.Attribute) and node.func.attr in ['with_name','with_suffix'] and len(node.args)==1:
                item,argument=value(node.func.value),value(node.args[0])
                if isinstance(item,Path) and isinstance(argument,str):return getattr(item,node.func.attr)(argument)
        return None
    for statement in tree.body:
        if isinstance(statement,(ast.Assign,ast.AnnAssign)):
            targets=statement.targets if isinstance(statement,ast.Assign)else[statement.target]
            resolved=value(statement.value)
            if resolved is not None:
                for target in targets:
                    if isinstance(target,ast.Name) and target.id!='ROOT':environment[target.id]=resolved
    found=set()
    for node in ast.walk(tree):
        if not isinstance(node,ast.Call):continue
        candidate=None;mode='r'
        if isinstance(node.func,ast.Attribute) and node.func.attr in ['read_text','read_bytes','open']:
            candidate=value(node.func.value)
            if node.func.attr=='open':
                mode=value(node.args[0])if node.args else'r'
                mode=next((value(item.value)for item in node.keywords if item.arg=='mode'),mode)
        elif isinstance(node.func,ast.Name) and node.func.id in ['read_json','open'] and node.args:
            candidate=value(node.args[0])
            if node.func.id=='open':
                mode=value(node.args[1])if len(node.args)>1 else'r'
                mode=next((value(item.value)for item in node.keywords if item.arg=='mode'),mode)
        if not isinstance(candidate,(str,Path))or not isinstance(mode,str)or not mode.startswith('r'):continue
        path=(root/Path(candidate)).resolve()
        if path.is_relative_to(root) and path.suffix.lower()=='.json':found.add(path.relative_to(root).as_posix())
    return found
