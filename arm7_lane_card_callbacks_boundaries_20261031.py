import qualified_arm7_card_scope_20261031 as qualified
import prove_arm7_lane_card_callbacks_scope_20261031 as scope
from project import ROOT


def boundaries(entry,layout):
    rows=qualified.guard(entry)
    address=int(entry['address'],0)
    row=scope.select((ROOT/entry['binary']).read_bytes(),address,entry['mode'],entry['bytes'])
    module=next(row for row in layout['modules'] if row['id']==entry['module'])
    if module['sha256']!=entry['inputModuleSha256']:raise ValueError('Source callback loader/module identity differs')
    return dict(qualifiedCanonicalScope=dict(qualified.REFERENCE),completeQualifiedRange=row,
        explicitInstructionBytes=row['instructionBytes'],explicitPoolBytes=row['poolBytes'],
        moduleLayoutCanonical=True,sourceCreditForScope=0,additionalInitializedDenominatorBytes=0,
        limitations='Qualified supplement closes these local boundaries; global unknown indirect producers and device completion remain unproved')
