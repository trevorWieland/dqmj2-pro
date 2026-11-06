#include "context_00.h"
BOOL native_main_02039954 (SNDWaveArc * waveArc, const SNDBankData * bank, int waveArcNo, u32 fileId, NNSSndHeapHandle heap)
{
    SNDInstPos pos = native_fn_0200a07c(bank);
    SNDInstData inst;
    ((void) 0) ;
    if (bank == ((void *)0) ) {
        ((void) 0) ;
        return 0 ;
    }
    while (native_fn_0200a09c(bank, &inst, &pos)) {
        if (inst.type == SND_INST_PCM && waveArcNo == inst.param.wave[1]) {
            if (!native_fn_0203988c(waveArc, inst.param.wave[0], fileId, heap)) {
                return 0 ;
            }
        }
    }
    return 1 ;
}
