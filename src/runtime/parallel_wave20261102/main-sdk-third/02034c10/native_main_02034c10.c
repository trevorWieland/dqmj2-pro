#include "context_00.h"
void native_main_02034c10 (NNSG2dAnimController * pAnimCtrl)
{
    ((void) 0) ;
    if ( IsReversePlayAnim_(pAnimCtrl)) {
        SequenceEdgeHandleReverse_(pAnimCtrl);
    } else {
        SequenceEdgeHandleNormal_(pAnimCtrl);
    }
    ValidateAnimFrame_(pAnimCtrl, &pAnimCtrl->pCurrent);
}
