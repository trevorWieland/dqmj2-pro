#include "context_00.h"
BOOL native_main_02039a14 (NNSSndHeapHandle heap)
{
    NNSSndArc * arc = native_fn_02038d78();
    int playerNo;
    const NNSSndArcPlayerInfo * playerInfo;
    ((void) 0) ;
    for (playerNo = 0; playerNo < 32 ; ++playerNo) {
        playerInfo = native_fn_02038f7c(playerNo);
        if (playerInfo == ((void *)0) ) continue;
        native_fn_02038008(playerNo, playerInfo->seqMax);
        native_fn_02038028(playerNo, playerInfo->allocChBitFlag);
        if (playerInfo->heapSize > 0 && heap != ((void *)0) ) {
            int i;
            for (i = 0; i < playerInfo->seqMax; i++) {
                if (!native_fn_02038040(playerNo, heap, playerInfo->heapSize)) {
                    return 0 ;
                }
            }
        }
    }
    return 1 ;
}
