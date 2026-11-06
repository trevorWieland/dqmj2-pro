import match_arm7
import qualified_arm7_card_scope_20261031 as qualified
import arm7_lane_card_callbacks_boundaries_20261031 as callbacks
from project import ROOT


def boundaries(entry,layout):
    address=int(entry['address'],0)
    qualified.guard(entry)
    if address in (0x038028e4,0x03802924,0x03802974):return callbacks.boundaries(entry,layout)
    spec=match_arm7.accepted_spec(entry,True)
    if spec['bytes']!=entry['bytes'] or spec['mode']!='arm':raise ValueError('Complete ordinary card canonical scope differs')
    code=entry['codeBytes']
    if {insn.address for insn in spec['instructions']}!=set(range(address,address+code,4)):
        raise ValueError('Card instruction/pool qualification differs')
    return dict(canonicalOriginalScope=True,completeAddress=entry['address'],completeBytes=entry['bytes'],
        instructionBytes=code,literalBytes=entry['bytes']-code,qualifiedCanonicalScope=dict(qualified.REFERENCE),
        originalModuleSha256=entry['inputModuleSha256'],additionalInitializedDenominatorBytes=0,
        limitations='Native complete function plus PC-relative pool extents; no whole-program indirect caller claim')
