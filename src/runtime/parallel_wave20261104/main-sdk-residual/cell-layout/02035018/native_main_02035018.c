#include "context_00.h"
void native_main_02035018 (NNSG2dCellAnimation * pCellAnim)
{
    const NNSG2dAnimDataSRT * pAnimResult = ((void *)0) ;
    const NNSG2dCellDataBank * pCellBank = ((void *)0) ;
    ((void) 0) ;
    ((void) 0) ;
    if ( pCellAnim->animCtrl.pActiveCurrent->frames == 0 ) {
        return;
    }
    pAnimResult = (const NNSG2dAnimDataSRT *)native_fn_02034d5c(&pCellAnim->animCtrl);
    ((void) 0) ;
    pAnimResult = (const NNSG2dAnimDataSRT *)native_fn_02034d5c(&pCellAnim->animCtrl);
    pCellBank = pCellAnim->pCellDataBank;
    ((void) 0) ;
    pCellAnim->pCurrentCell = native_fn_020349f4(pCellBank, pAnimResult->index);
    ((void) 0) ;
    {
        const NNSG2dAnimationElement elemType = NNSi_G2dGetAnimSequenceElementType(pCellAnim->animCtrl.pAnimSequence->animType);
        native_fn_020372f8(&pCellAnim->srtCtrl, NNS_G2D_SRTCONTROLTYPE_SRT);
        if ( elemType != NNS_G2D_ANIMELEMENT_INDEX ) {
            if ( elemType == NNS_G2D_ANIMELEMENT_INDEX_T ) {
                const NNSG2dAnimDataT * pAnmResT = (const NNSG2dAnimDataT *)pAnimResult;
                native_fn_02037294(&pCellAnim->srtCtrl, pAnmResT->py, pAnmResT->px);
            } else {
                native_fn_020372d8(&pCellAnim->srtCtrl, pAnimResult->sx, pAnimResult->sy);
                native_fn_020372b8(&pCellAnim->srtCtrl, pAnimResult->rotZ);
                native_fn_02037294(&pCellAnim->srtCtrl, pAnimResult->py, pAnimResult->px);
            }
        }
    }
    if ( NNS_G2dCellDataBankHasVramTransferData(pCellBank) &&
         NNSi_G2dIsCellAnimVramTransferHandleValid(pCellAnim)) {
        const NNSG2dCellVramTransferData * pCellTransferData = NNSi_G2dGetCellVramTransferData(pCellBank, pAnimResult->index);
        native_fn_02035518(pCellAnim->cellTransferStateHandle,
                                             pCellTransferData->srcDataOffset,
                                             pCellTransferData->szByte);
    }
}
