import struct

from overlay_oracle003_shared_render import seed_shared_render003, shared_render_call003, assert_shared_render003

STARTS={0x021D8D68:'func_02062a50',0x021D8F80:'func_02062a88',0x021D9198:'func_020c3828',0x021D939C:'func_020c3904'}
FINISHES={0x021D8F6C,0x021D9184,0x021D9388,0x021D958C}


def seed_panel_lifecycle003(engine,address,vector):
    if address not in STARTS and address not in FINISHES:return seed_shared_render003(engine,address,vector)
    before=bytes(engine.mem_read(0x021E057C,16))
    values=[0xFFFFFFFF if vector//8%3==0 else (0 if vector//8%3==1 else 0x80000000+index*0x12345) for index in range(3)]
    for index,value in enumerate(values):engine.mem_write(0x03007014+index*256,struct.pack('<I',value))
    return {'before':before,'values':values,'mask':vector%8,'getters':0}


def panel_lifecycle_call003(engine,address,name,value,state):
    if address not in STARTS:return shared_render_call003(engine,address,name,value,state)
    if name==STARTS[address]:
        index=state['getters'];state['getters']+=1
        if index>=3:raise ValueError('Panel table traversal exceeded three rows')
        if name in {'func_02062a50','func_02062a88'}:return 0x03007000+index*256 if state['mask']>>index&1 else 0
        return state['values'][index]
    return value


def assert_panel_lifecycle003(engine,address,args,calls,state):
    if address not in STARTS and address not in FINISHES:return assert_shared_render003(engine,address,args,calls,state)
    before=bytearray(state['before'])
    if address in FINISHES:expected=['func_ov003_021d9dc0','func_ov003_021d9c60','func_ov003_021d9e40']
    else:
        getter=STARTS[address];record=getter in {'func_02062a50','func_02062a88'}
        expected=['func_020c39d0','func_02061260','func_02061bf0','func_ov003_021d95a0']+[getter]*3
        if calls[0]['args'][0]!=2 or calls[1]['args'][0]!=0:raise ValueError('Panel startup mode/cleanup arguments differ')
        if [c['args'][0] for c in calls if c['name']==getter]!=[0,1,2] or state['getters']!=3:raise ValueError('Panel startup indexed record/identifier getter differs')
        values=[value if not record or state['mask']>>index&1 else 0xFFFFFFFF for index,value in enumerate(state['values'])]
        before[:3]=bytes([0,int(record),0]);before[4:16]=struct.pack('<3I',*values)
    if [c['name'] for c in calls]!=expected or bytes(engine.mem_read(0x021E057C,16))!=bytes(before):raise ValueError('Panel lifecycle complete table/flags/call order differs')
