import json
import main_sdk_dma_async152_engine_20261101 as engine

ENTRY=0x0200867C
RECORDS=0x020E335C


def setup(case,seed=0,bodies=None):
    machine=engine.setup(bodies or {},seed,case.get('control',0));cpu=machine['cpu']
    for address,width,value in[(0x04000208,2,case.get('master',1)),(0x04000210,4,case.get('ie',0)),
        (0x040000B8+12*case['channel'],4,0x80000000 if case.get('busy')else 0x1234)]:
        cpu.mem_write(address,value.to_bytes(width,'little'))
    arguments=[case['channel'],case.get('source',engine.DATA+0x1000),case.get('destination',engine.DATA+0x2000),
        case['bytes'],case.get('callback',0),case.get('argument',0)]
    return machine,arguments


def main():
    for channel in range(4):
        for size in(0,4):
            for callback in(0,0x02008008):
                machine,args=setup({'channel':channel,'bytes':size,'callback':callback})
                r=machine['invoke'](ENTRY,args,10000)
                print(json.dumps({'channel':channel,'bytes':size,'callback':hex(callback),'actualReturn':r['actualReturn'],
                    'error':r['error'],'pc':r['pc'],'rawR0':r['registers'][0],
                    'stores':[x for x in r['writes']if not engine.STACK<=x[0]<engine.STACK+0x4000]}),flush=True)


if __name__=='__main__':main()
