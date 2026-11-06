from wave20261104_main_tail_bindings import verify_original as branch_verify


def verify_original(row,bindings):
    if (row.get('program') or '',row['processor'],row['module'],row['mode'],row['address'],row['bytes'])!=('','arm9','main','arm','0x207d74c',312):raise ValueError('Exact conditional result caller identity differs')
    if len(row['relocations'])!=6 or any(r['type'] not in (1,28,29) for r in row['relocations']):raise ValueError('Exact six original conditional result branches differ')
    return branch_verify(row,bindings)
