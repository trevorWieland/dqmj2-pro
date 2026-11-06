#include "context_00.h"
NNSSndArcLoadResult native_main_020393cc (int waveArcNo, u32 loadFlag, NNSSndHeapHandle heap, BOOL bSetAddr, struct SNDWaveArc ** pData)
{
    const NNSSndArcWaveArcInfo * waveArcInfo;
    SNDWaveArc * waveArc = ((void *)0) ;
    waveArcInfo = native_fn_02038eb4(waveArcNo);
    if (waveArcInfo == ((void *)0) ) return NNS_SND_ARC_LOAD_ERROR_INVALID_WAVEARC_NO;
    if (loadFlag & (1 << 2) ) {
        if (waveArcInfo->flags & (1 << 0) ) {
            waveArc = native_fn_0203963c(waveArcInfo->fileId, heap, bSetAddr);
        } else {
            waveArc = native_fn_020395d0(waveArcInfo->fileId, heap, bSetAddr);
        }
        if (waveArc == ((void *)0) ) {
            return NNS_SND_ARC_LOAD_ERROR_FAILED_LOAD_WAVE;
        }
    } else {
        waveArc = (SNDWaveArc *)native_fn_0203917c(waveArcInfo->fileId);
    }
    if (pData != ((void *)0) ) *pData = waveArc;
    return NNS_SND_ARC_LOAD_SUCESS;
}
