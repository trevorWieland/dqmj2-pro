#include "context_00.h"
void native_main_0202fde0 (NNSG3dRS * rs, u32 opt, const NNSG3dResMatData * mat, u32 idxMat)
{
    BOOL cbFlag;
    NNSG3dSbcCallBackTiming cbTiming;
    ((void) 0) ;
    ((void) 0) ;
    rs->currentMat = (u8)idxMat;
    rs->flag |= NNS_G3D_RSFLAG_CURRENT_MAT_VALID;
    rs->pMatAnmResult = &rs->tmpMatAnmResult;
    cbFlag = NNSi_G3dCallBackCheck_A(rs, 0x04 , &cbTiming);
    if (!cbFlag) {
        NNSG3dMatAnmResult * pResult;
        if (rs->pRenderObj->recMatAnm &&
            !(rs->flag & NNS_G3D_RSFLAG_OPT_RECORD)) {
            pResult = (rs->pRenderObj->recMatAnm + idxMat);
        } else {
            if ((opt == 0x20 || opt == 0x40 ) &&
                NNSi_G3dBitVecCheck(&rs->isMatCached[0], idxMat)) {
                if (rs->pRenderObj->recMatAnm) {
                    pResult = (rs->pRenderObj->recMatAnm + idxMat);
                } else {
                    pResult = &native_data_main_020ee1f4.field_0004.matCache[idxMat];
                }
            } else {
                if (rs->pRenderObj->recMatAnm) {
                    NNSi_G3dBitVecSet(&rs->isMatCached[0], idxMat);
                    pResult = (rs->pRenderObj->recMatAnm + idxMat);
                } else if (opt == 0x40 )   {
                    NNSi_G3dBitVecSet(&rs->isMatCached[0], idxMat);
                    pResult = &native_data_main_020ee1f4.field_0004.matCache[idxMat];
                } else {
                    pResult = &rs->tmpMatAnmResult;
                }
                {
                    pResult->flag = (NNSG3dMatAnmResultFlag) 0;
                    if (NNS_G3dGetMatDataByIdx(rs->pResMat, idxMat)->flag & NNS_G3D_MATFLAG_WIREFRAME) {
                        pResult->flag |= NNS_G3D_MATANM_RESULTFLAG_WIREFRAME;
                    }
                }
                {
                    u32 mask = native_data_main_020d9068.masks[(mat->flag >> 6) & 7];
                    pResult->prmMatColor0 = (native_data_main_020edf90.prmMatColor0 & ~mask) |
                                            (mat->diffAmb & mask);
                }
                {
                    u32 mask = native_data_main_020d9068.masks[(mat->flag >> 9) & 7];
                    pResult->prmMatColor1 = (native_data_main_020edf90.prmMatColor1 & ~mask) |
                                            (mat->specEmi & mask);
                }
                pResult->prmPolygonAttr = (native_data_main_020edf90.prmPolygonAttr & ~mat->polyAttrMask) |
                                          (mat->polyAttr & mat->polyAttrMask);
                pResult->prmTexImage = mat->texImageParam;
                pResult->prmTexPltt = mat->texPlttBase;
                if (mat->flag & NNS_G3D_MATFLAG_TEXMTX_USE) {
                    const u8 * p = (const u8 *)mat + sizeof(NNSG3dResMatData);
                    if (!(mat->flag & NNS_G3D_MATFLAG_TEXMTX_SCALEONE)) {
                        const fx32 * p_fx32 = (const fx32 *)p;
                        pResult->scaleS = *(p_fx32 + 0);
                        pResult->scaleT = *(p_fx32 + 1);
                        p += 2 * sizeof(fx32);
                    } else {
                        pResult->flag |= NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE;
                    }
                    if (!(mat->flag & NNS_G3D_MATFLAG_TEXMTX_ROTZERO)) {
                        const fx16 * p_fx16 = (const fx16 *)p;
                        pResult->sinR = *(p_fx16 + 0);
                        pResult->cosR = *(p_fx16 + 1);
                        p += 2 * sizeof(fx16);
                    } else {
                        pResult->flag |= NNS_G3D_MATANM_RESULTFLAG_TEXMTX_ROTZERO;
                    }
                    if (!(mat->flag & NNS_G3D_MATFLAG_TEXMTX_TRANSZERO)) {
                        const fx32 * p_fx32 = (const fx32 *)p;
                        pResult->transS = *(p_fx32 + 0);
                        pResult->transT = *(p_fx32 + 1);
                    } else {
                        pResult->flag |= NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO;
                    }
                    pResult->flag |= NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SET;
                }
                ((void) 0) ;
                if (rs->pRenderObj->anmMat &&
                    NNSi_G3dBitVecCheck(&rs->pRenderObj->hintMatAnmExist[0], idxMat)) {
                    (void)(*rs->pRenderObj->funcBlendMat)(pResult, rs->pRenderObj->anmMat, idxMat);
                }
                if (pResult->flag & (NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SET |
                                     NNS_G3D_MATANM_RESULTFLAG_TEXMTX_MULT)) {
                    pResult->origWidth = mat->origWidth;
                    pResult->origHeight = mat->origHeight;
                    pResult->magW = mat->magW;
                    pResult->magH = mat->magH;
                }
            }
        }
        rs->pMatAnmResult = pResult;
    }
    cbFlag = NNSi_G3dCallBackCheck_B(rs, 0x04 , &cbTiming);
    if (!cbFlag) {
        NNSG3dMatAnmResult * pResult;
        ((void) 0) ;
        pResult = rs->pMatAnmResult;
        if (pResult->prmPolygonAttr & 0x001f0000 ) {
            if (pResult->flag & NNS_G3D_MATANM_RESULTFLAG_WIREFRAME) {
                pResult->prmPolygonAttr &= ~0x001f0000 ;
            }
            rs->flag &= ~NNS_G3D_RSFLAG_MAT_TRANSPARENT;
            if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD)) {
                u32 cmd[7];
                cmd[0] = ((u32)((0x30) | (( 0x31) << 8) | (( 0x29) << 16) | (( 0x00) << 24))) ;
                cmd[1] = pResult->prmMatColor0;
                cmd[2] = pResult->prmMatColor1;
                cmd[3] = pResult->prmPolygonAttr;
                cmd[4] = ((u32)((0x2a) | (( 0x2b) << 8) | (( 0x00) << 16) | (( 0x00) << 24))) ;
                cmd[5] = pResult->prmTexImage;
                cmd[6] = pResult->prmTexPltt;
                NNS_G3dGeBufferData_N(&cmd[0], 7);
                if (pResult->flag & (NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SET |
                                     NNS_G3D_MATANM_RESULTFLAG_TEXMTX_MULT)) {
                    ((void) 0) ;
                    (*rs->funcTexMtx)(pResult);
                }
            }
        } else {
            rs->flag |= NNS_G3D_RSFLAG_MAT_TRANSPARENT;
        }
    }
    (void) NNSi_G3dCallBackCheck_C(rs, 0x04 , cbTiming);
}
