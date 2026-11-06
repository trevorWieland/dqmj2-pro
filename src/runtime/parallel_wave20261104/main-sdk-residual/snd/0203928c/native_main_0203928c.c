#include "context_00.h"
NNSSndArcLoadResult native_main_0203928c (int bankNo, u32 loadFlag, NNSSndHeapHandle heap, BOOL bSetAddr, struct SNDBankData ** pData)
{
    const NNSSndArcBankInfo * bankInfo;
    const NNSSndArcWaveArcInfo * waveArcInfo;
    SNDBankData * bank = ((void *)0) ;
    SNDWaveArc * waveArc;
    NNSSndArcLoadResult result;
    int i;
    bankInfo = native_fn_02038e50(bankNo);
    if (bankInfo == ((void *)0) ) return NNS_SND_ARC_LOAD_ERROR_INVALID_BANK_NO;
    if (loadFlag & (1 << 1) ) {
        bank = native_fn_02039564(bankInfo->fileId, heap, bSetAddr);
        if (bank == ((void *)0) ) {
            return NNS_SND_ARC_LOAD_ERROR_FAILED_LOAD_BANK;
        }
    } else {
        bank = (SNDBankData *)native_fn_0203917c(bankInfo->fileId);
    }
    for (i = 0; i < 4 ; i++) {
        if (bankInfo->waveArcNo[i] == 0xffff ) continue;
        waveArcInfo = native_fn_02038eb4(bankInfo->waveArcNo[i]);
        if (waveArcInfo == ((void *)0) ) return NNS_SND_ARC_LOAD_ERROR_INVALID_WAVEARC_NO;
        result = native_fn_020393cc(bankInfo->waveArcNo[i], loadFlag, heap, bSetAddr, &waveArc);
        if (result != NNS_SND_ARC_LOAD_SUCESS) return result;
        if (waveArcInfo->flags & (1 << 0) ) {
            if (loadFlag & (1 << 2) ) {
                if (!native_fn_02039954(waveArc, bank, i, waveArcInfo->fileId, heap)) {
                    return NNS_SND_ARC_LOAD_ERROR_FAILED_LOAD_WAVE;
                }
            }
        }
        if (bank != ((void *)0) && waveArc != ((void *)0) ) {
            native_fn_02009ed0(bank, i, waveArc);
        }
    }
    if (pData != ((void *)0) ) *pData = bank;
    return NNS_SND_ARC_LOAD_SUCESS;
}
