#include "context_00.h"
BOOL native_main_02034d68 (NNSG2dAnimController * pAnimCtrl, fx32 frames)
{
    BOOL bChangeFrame = 0 ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    if ( pAnimCtrl->bActive != 1 ) {
        return 0 ;
    }
    pAnimCtrl->currentTime += native_fn_0201af84(FX_MulInline(pAnimCtrl->speed, frames) );
    while ( ShouldAnmCtrlMoveNext_(pAnimCtrl)) {
        bChangeFrame = 1 ;
        pAnimCtrl->currentTime -= ((fx32) 0x0000000000001000L) * (int)pAnimCtrl->pCurrent->frames;
        MoveNext_(pAnimCtrl);
        if ( IsReachEdge_(pAnimCtrl, pAnimCtrl->pCurrent)) {
            native_fn_02034c10(pAnimCtrl);
        }
        if ( pAnimCtrl->pCurrent->frames != 0 ) {
            pAnimCtrl->pActiveCurrent = pAnimCtrl->pCurrent;
        }
        if ( pAnimCtrl->callbackFunctor.type != NNS_G2D_ANMCALLBACKTYPE_NONE ) {
            CallbackFuncHandling_(&pAnimCtrl->callbackFunctor, GetCurrentFrameIdx_(pAnimCtrl));
        }
    }
    return bChangeFrame;
}
