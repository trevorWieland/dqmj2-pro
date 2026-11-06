import ast
import inspect
import re
from project import ROOT,sha256


def install(unit):
    if not unit.WORK.resolve().is_relative_to((ROOT/'work').resolve()):raise ValueError('Generated-only experiment must stay under work')
    if hasattr(unit,'_generated_word_hypothesis_policy'):return unit._generated_word_hypothesis_policy
    tree=ast.parse(inspect.getsource(unit.source_text));function=tree.body[0];removed=[];body=[]
    for statement in function.body:
        if isinstance(statement,ast.If) and ast.unparse(statement.test)=='len(result.splitlines()) > 500':removed.append(statement)
        else:body.append(statement)
    assert len(removed)==1
    function.body=body;function.name='_source_text_generated_word_hypothesis'
    namespace={};exec(compile(ast.fix_missing_locations(tree),'<generated-word-source>', 'exec'),unit.__dict__,namespace)
    generated=namespace[function.name]
    def transform(draft,original):
        return generated(re.sub(r'\bM2C_UNK\b','u32',draft),original)
    unit.source_text=transform
    policy={'sourceCredit':0,'generatedHypothesisOnly':True,'unknownTypeTokensHypothesizedAsUnsigned32':True,'stackObjectWidthsStillUnqualified':True,'untranslatedLogicMacrosStillRejected':True,'acceptedSourceLineLimitUnchanged':500,'generatedOutputLineCapDeferred':True,'frozenFrameworkSha256':sha256(ROOT/'draft_runtime.py'),'experimentSha256':sha256(ROOT/'generated_word_type_hypotheses_20261031.py')}
    unit._generated_word_hypothesis_policy=policy
    return policy
