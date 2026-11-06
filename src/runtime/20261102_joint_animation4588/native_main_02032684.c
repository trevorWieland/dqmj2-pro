#include "types_02032684.h"

void native_main_02032684 (const NNSG3dResJntAnm * pJntAnm, u32 dataIdx, fx32 Frame, NNSG3dJntAnmResult * pResult)
{
    NNSG3dResJntAnmSRTTag * pAnmSRTTag;
    NNSG3dJntAnmSRTTag tag;
    const u32 * pData;
    BOOL IsDecimalFrame;
    fx32 pS_invS[6];
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0)
                   ;
    {
        const u16 * ofsTag = (const u16 *)((u8 *) pJntAnm + sizeof(NNSG3dResJntAnm));
        pAnmSRTTag = (NNSG3dResJntAnmSRTTag *)((u8 *) pJntAnm + ofsTag[dataIdx]);
        tag = (NNSG3dJntAnmSRTTag)pAnmSRTTag->tag;
    }
    if (tag & NNS_G3D_JNTANM_SRTINFO_IDENTITY) {
        pResult->flag = (NNSG3dJntAnmResultFlag)(NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE |
                                                 NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO |
                                                 NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO);
        goto GET_JOINTSCALE;
    }
    pData = (const u32 *)((const u8 *)pAnmSRTTag + sizeof(NNSG3dResJntAnmSRTTag));
    IsDecimalFrame = (BOOL)((Frame & (((fx32) 0x0000000000001000L) - 1)) &&
                            (pJntAnm->flag & NNS_G3D_JNTANM_OPTION_INTERPOLATION));
    pResult->flag = (NNSG3dJntAnmResultFlag) 0;
    if (!(tag & (NNS_G3D_JNTANM_SRTINFO_IDENTITY_T | NNS_G3D_JNTANM_SRTINFO_BASE_T))) {
        if (!(tag & NNS_G3D_JNTANM_SRTINFO_CONST_TX)) {
            if (IsDecimalFrame) {
                native_fn_02032b90(&pResult->trans.x,
                                Frame,
                                pData,
                                pJntAnm);
            } else {
                native_fn_02032a38(&pResult->trans.x,
                              Frame,
                              pData,
                              pJntAnm);
            }
            pData += 2;
        } else {
            pResult->trans.x = *(fx32 *)pData;
            pData += 1;
        }
        if (!(tag & NNS_G3D_JNTANM_SRTINFO_CONST_TY)) {
            if (IsDecimalFrame) {
                native_fn_02032b90(&pResult->trans.y,
                                Frame,
                                pData,
                                pJntAnm);
            } else {
                native_fn_02032a38(&pResult->trans.y,
                              Frame,
                              pData,
                              pJntAnm);
            }
            pData += 2;
        } else {
            pResult->trans.y = *(fx32 *)pData;
            pData += 1;
        }
        if (!(tag & NNS_G3D_JNTANM_SRTINFO_CONST_TZ)) {
            if (IsDecimalFrame) {
                native_fn_02032b90(&pResult->trans.z,
                                Frame,
                                pData,
                                pJntAnm);
            } else {
                native_fn_02032a38(&pResult->trans.z,
                              Frame,
                              pData,
                              pJntAnm);
            }
            pData += 2;
        } else {
            pResult->trans.z = *(fx32 *)pData;
            pData += 1;
        }
    } else {
        if (tag & NNS_G3D_JNTANM_SRTINFO_IDENTITY_T) {
            pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO;
        } else {
            native_fn_020323dc(pResult);
        }
    }
    if (!(tag & (NNS_G3D_JNTANM_SRTINFO_IDENTITY_R | NNS_G3D_JNTANM_SRTINFO_BASE_R))) {
        if (!(tag & NNS_G3D_JNTANM_SRTINFO_CONST_R)) {
            if (IsDecimalFrame) {
                native_fn_02033480(&pResult->rot,
                              Frame,
                              pData,
                              pJntAnm);
            } else {
                native_fn_02033068(&pResult->rot,
                            Frame,
                            pData,
                            pJntAnm);
            }
            pData += 2;
        } else {
            if (native_fn_020337c4(&pResult->rot,
                                 (void *)((u8 *)pJntAnm + pJntAnm->ofsRot3),
                                 (void *)((u8 *)pJntAnm + pJntAnm->ofsRot5),
                                 (NNSG3dJntAnmRIdx) * pData)) {
                vecCross_((const VecFx32 *)&pResult->rot._00,
                          (const VecFx32 *)&pResult->rot._10,
                          (VecFx32 *)&pResult->rot._20);
            }
            pData += 1;
        }
    } else {
        if (tag & NNS_G3D_JNTANM_SRTINFO_IDENTITY_R) {
            pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO;
        } else {
            native_fn_02032504(pResult);
        }
    }
    if (!(tag & (NNS_G3D_JNTANM_SRTINFO_IDENTITY_S | NNS_G3D_JNTANM_SRTINFO_BASE_S))) {
        if (!(tag & NNS_G3D_JNTANM_SRTINFO_CONST_SX)) {
            fx32 sx_invsx[2];
            if (IsDecimalFrame) {
                native_fn_02032ed4(&sx_invsx[0],
                                Frame,
                                pData,
                                pJntAnm);
            } else {
                native_fn_02032cec(&sx_invsx[0],
                              Frame,
                              pData,
                              pJntAnm);
            }
            *(pS_invS + 0) = sx_invsx[0];
            *(pS_invS + 3) = sx_invsx[1];
        } else {
            const fx32 * p_fx32 = (const fx32 *)pData;
            *(pS_invS + 0) = *(p_fx32 + 0);
            *(pS_invS + 3) = *(p_fx32 + 1);
        }
        pData += 2;
        if (!(tag & NNS_G3D_JNTANM_SRTINFO_CONST_SY)) {
            fx32 sy_invsy[2];
            if (IsDecimalFrame) {
                native_fn_02032ed4(&sy_invsy[0],
                                Frame,
                                pData,
                                pJntAnm);
            } else {
                native_fn_02032cec(&sy_invsy[0],
                              Frame,
                              pData,
                              pJntAnm);
            }
            *(pS_invS + 1) = sy_invsy[0];
            *(pS_invS + 4) = sy_invsy[1];
        } else {
            const fx32 * p_fx32 = (const fx32 *)pData;
            *(pS_invS + 1) = *(p_fx32 + 0);
            *(pS_invS + 4) = *(p_fx32 + 1);
        }
        pData += 2;
        if (!(tag & NNS_G3D_JNTANM_SRTINFO_CONST_SZ)) {
            fx32 sz_invsz[2];
            if (IsDecimalFrame) {
                native_fn_02032ed4(&sz_invsz[0],
                                Frame,
                                pData,
                                pJntAnm);
            } else {
                native_fn_02032cec(&sz_invsz[0],
                              Frame,
                              pData,
                              pJntAnm);
            }
            *(pS_invS + 2) = sz_invsz[0];
            *(pS_invS + 5) = sz_invsz[1];
        } else {
            const fx32 * p_fx32 = (const fx32 *)pData;
            *(pS_invS + 2) = *(p_fx32 + 0);
            *(pS_invS + 5) = *(p_fx32 + 1);
        }
        pData += 2;
    } else {
        if (tag & NNS_G3D_JNTANM_SRTINFO_IDENTITY_S) {
            pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE;
        } else {
            native_fn_02032474(pResult);
            return;
        }
    }
GET_JOINTSCALE:
    (*native_data_020ee1f4->funcJntScale)(
        pResult,
        pS_invS,
        native_data_020ee1f4->c,
        ((pResult->flag & NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE) ?
         NNS_G3D_SRTFLAG_SCALE_ONE :
         0)
        );
}
void native_fn_02032a38 (fx32 * pVal, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
void native_fn_02032b90 (fx32 * pVal, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
void native_fn_02032cec (fx32 * s_invs, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
void native_fn_02032ed4 (fx32 * s_invs, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
void native_fn_02033068 (MtxFx33 * pRot, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
void native_fn_02033480 (MtxFx33 * pRot, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
BOOL native_fn_020337c4 (MtxFx33 * pRot, const void * pArrayRot3, const void * pArrayRot5, NNSG3dJntAnmRIdx info);
