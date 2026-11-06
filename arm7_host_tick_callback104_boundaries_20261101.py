import link_arm7_host_tick_callback104_scope_20261101 as scope


def boundaries(entry,layout):
    boundary=scope.guard(entry)
    return {'inventorySha256':boundary['inventorySha256'],'originalFullGapScopeQualified':True,'instructionBytes':88,
        'generatedLiteralBytes':16,'literalReferences':boundary['literalWords'],'outsideRootReferences':boundary['alignedRootPointerWords'],
        'outsideInteriorOrPoolReferences':[],'paddingCredit':0,'instructionMode':'arm',
        'tailDestination':boundary['tailDestination'],'initializedDenominatorDelta':0,
        'limitations':['Fresh original direct/aligned-word boundary proof; opaque computed producers outside the bounded entry domain remain unresolved']}
