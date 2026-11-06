import ast
import inspect
from project import ROOT,sha256
import oracle_source_closure_v2_20261106 as base


def main():
    output=ROOT/'oracle_source_closure_v3_20261106.py'
    if output.exists():raise ValueError('New collector path is already materialized')
    tree=ast.parse(inspect.getsource(base.collect));function=tree.body[0]
    class Replace(ast.NodeTransformer):
        def visit_Call(self,node):
            node=self.generic_visit(node)
            if isinstance(node.func,ast.Attribute) and node.func.attr in ['resolve','is_file'] and not node.args and not node.keywords:return ast.Call(ast.Attribute(ast.Name('lookup',ast.Load()),node.func.attr,ast.Load()),[node.func.value],[])
            if isinstance(node.func,ast.Name) and node.func.id in ['sha256','read_json'] and not (node.func.id=='sha256' and ast.dump(node.args[0])==ast.dump(ast.parse("ROOT/'oracle_source_closure_20261031.py'",mode='eval').body)):node.func=ast.Attribute(ast.Name('lookup',ast.Load()),'hash' if node.func.id=='sha256' else 'read_json',ast.Load())
            return node
    tree=Replace().visit(tree);function=tree.body[0];function.body[1:1]=ast.parse("if sha256(ROOT/'oracle_source_closure_v2_20261106.py')!=V2_SHA256:raise ValueError('Pinned qualifiedv2source closure collector changed')\nlookup=PathLookupEpoch(ROOT)").body
    returned=function.body.pop()
    if not isinstance(returned,ast.Return):raise ValueError('Base collector return shape changed')
    function.body+=ast.parse('result=None\nlookup.verify()\nreturn result').body;function.body[-3].value=returned.value;ast.fix_missing_locations(tree)
    header="import ast\nimport hashlib\nimport json\nimport re\nimport subprocess\nfrom project import ROOT,read_json,write_json,sha256\nfrom static_json_reads_20261031 import required_json_reads\nfrom oracle_source_closure_v2_20261106 import LEGACY_SHA256,EXCLUDED,SKIP,EXTENSIONS,_parent_requires_hashes\nfrom collector_path_lookup_epoch_20261106 import PathLookupEpoch\nV2_SHA256="+repr(sha256(ROOT/'oracle_source_closure_v2_20261106.py'))+"\nSEARCH=[ROOT,ROOT/'evidence/application',ROOT/'evidence/encounter',ROOT/'evidence/save',ROOT/'nonmatching/encounter']\n\n\n"
    output.write_text(header+ast.unparse(tree)+'\n',encoding='utf-8');print(dict(path=output.name,sha256=sha256(output)))


if __name__=='__main__':main()
