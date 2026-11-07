import copy
from project import sha256
from source_packet_contracts import local

def validate_alias_revision(old,new,contract):
    if old.get('matches') or new.get('matches') or old.get('functionMatches') or new.get('functionMatches'):
        raise ValueError('Alias-only revision cannot contain functions')
    if len(old.get('dataMatches',[])) != 1 or len(new.get('dataMatches',[])) != 1:
        raise ValueError('Exactly one typed-data record required')
    prior,actual = old['dataMatches'][0],new['dataMatches'][0]
    expected = copy.deepcopy(prior)
    expected['dataAliases'] = contract['aliases']
    if actual != expected:
        raise ValueError('Only the reviewed four-entry dataAliases map may change')
    scope = contract['namespace']
    for field in ('program','processor','module','kind','mode','address','bytes'):
        value = actual.get(field,old.get(field))
        if field == 'program': value = value or ''
        if value != scope[field]:
            raise ValueError('Alias revision changed its data namespace/extent: '+field)
    if old['romSha256'] != new['romSha256'] or new.get('allPassed') is not True:
        raise ValueError('Original ROM/success namespace changed')
    for field in ('sourceSha256','objectSha256','targetSha256'):
        key = 'compilerObjectSha256' if field == 'objectSha256' else field
        if actual[field] != contract[key]:
            raise ValueError('Original source/object/target contract changed')
    for field in ('source','object','compiler'):
        if sha256(local(actual[field])) != actual[field+'Sha256']:
            raise ValueError('Original data input changed: '+field)
    begin,end = int(actual['address'],0),int(actual['address'],0)+actual['bytes']
    if len(contract['aliases']) != 4 or any(not begin <= int(address,0) < end for address in contract['aliases'].values()):
        raise ValueError('Alias extent is outside the source object')
    return actual

def compose_specification(spec,old_report,new_report,producer):
    result = copy.deepcopy(spec)
    targets = [row for row in result['packets'] if row['report']==old_report]
    if len(targets) != 1 or old_report==new_report:
        raise ValueError('Exactly one additive pending packet replacement required')
    targets[0]['report'],targets[0]['producer'] = new_report,list(producer)
    return result
