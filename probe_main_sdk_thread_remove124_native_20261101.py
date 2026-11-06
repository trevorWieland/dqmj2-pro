import json
import main_sdk_thread_remove124_engine_20261101 as engine

G=0x020E33C0
TARGET,CURRENT,QUEUE,WAITER,MUTEX,ALARM=engine.DATA+0x800,engine.DATA+0xA00,engine.DATA+0xC00,engine.DATA+0xE00,engine.DATA+0x1000,engine.DATA+0x1200


def setup(case,seed=0,bodies=None):
    machine=engine.setup(bodies or {},seed,case.get('control',0));cpu=machine['cpu']
    def put(a,n,v):cpu.mem_write(a,v.to_bytes(n,'little'))
    cpu.mem_write(G,bytes(0x40));cpu.mem_write(TARGET,bytes(0xB4));cpu.mem_write(CURRENT,bytes(0xB4))
    put(G+4,4,case.get('count',0));put(G+8,4,G+0x28);put(G+0x26,2,case.get('depth',0));put(G+0x28,4,CURRENT)
    put(CURRENT+0x64,4,1);put(TARGET+0x64,4,case.get('state',0))
    if case.get('order',0):put(G+0x2C,4,CURRENT);put(CURRENT+0x68,4,TARGET)
    else:put(G+0x2C,4,TARGET);put(TARGET+0x68,4,CURRENT)
    features=case.get('features','empty')
    if features in('queue','all'):
        cpu.mem_write(QUEUE,bytes(8));put(QUEUE,4,TARGET);put(QUEUE+4,4,TARGET);put(TARGET+0x78,4,QUEUE)
    if features in('join','all'):
        cpu.mem_write(WAITER,bytes(0xB4));put(TARGET+0x9C,4,WAITER);put(TARGET+0xA0,4,WAITER)
        put(WAITER+0x78,4,TARGET+0x9C);put(WAITER+0x64,4,0)
    if features in('mutex','all'):
        cpu.mem_write(MUTEX,bytes(24));put(TARGET+0x88,4,MUTEX);put(TARGET+0x8C,4,MUTEX)
        put(MUTEX+8,4,TARGET);put(MUTEX+0xC,4,3)
    if features in('alarm','all'):
        cpu.mem_write(ALARM,bytes(0x28));put(TARGET+0xB0,4,ALARM)
    if case.get('currentTarget'):put(G+0x28,4,TARGET)
    return machine


def main():
    for features in('empty','queue','join','mutex','alarm','all'):
        machine=setup({'features':features});r=machine['invoke'](0x020067FC,[TARGET],10000)
        print(json.dumps({'features':features,'actualReturn':r['actualReturn'],'error':r['error'],'pc':r['pc'],
            'rawReturn':r['registers'][0],'stores':[x for x in r['writes']if not engine.STACK<=x[0]<engine.STACK+0x4000],
            'nestedReturns':r['nestedReturns']}),flush=True)


if __name__=='__main__':main()
