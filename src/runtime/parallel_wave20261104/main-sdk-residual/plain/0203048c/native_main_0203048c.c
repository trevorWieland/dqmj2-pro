#include "context_00.h"
void native_main_0203048c (NNSG3dRS * rs, u32 opt)
{
    u32 cmdLen = 4;
    BOOL cbFlag;
    NNSG3dSbcCallBackTiming cbTiming;
    u32 idxNode = *(rs->c + 1);
    rs->currentNodeDesc = (u8)idxNode;
    rs->flag |= NNS_G3D_RSFLAG_CURRENT_NODEDESC_VALID;
    ((void) 0) ;
    if (rs->flag & NNS_G3D_RSFLAG_OPT_SKIP_SBCMTXCALC) {
        if (opt == 0x40 ||
            opt == 0x60 ) {
            ++cmdLen;
        }
        if (opt == 0x20 ||
            opt == 0x60 ) {
            ++cmdLen;
            if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD)) {
                u32 idxMtxDest = *(rs->c + 4);
                ((void) 0) ;
                native_fn_0202e434(0x14 ,
                                    &idxMtxDest,
                                    1 );
            }
        }
        rs->c += cmdLen;
        return;
    }
    {
        if (opt == 0x40 ||
            opt == 0x60 ) {
            u32 idxMtxSrc;
            ++cmdLen;
            if (opt == 0x40 ) {
                idxMtxSrc = *(rs->c + 4);
            } else {
                idxMtxSrc = *(rs->c + 5);
            }
            ((void) 0) ;
            if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD)) {
                native_fn_0202e434(0x14 ,
                                    &idxMtxSrc,
                                    1 );
            }
        }
    }
    rs->pJntAnmResult = &rs->tmpJntAnmResult;
    cbFlag = NNSi_G3dCallBackCheck_A(rs, 0x06 , &cbTiming);
    if (!cbFlag) {
        NNSG3dJntAnmResult * pAnmResult;
        BOOL isUseRecordData;
        if (rs->pRenderObj->recJntAnm) {
            pAnmResult = (rs->pRenderObj->recJntAnm + idxNode);
            if (!(rs->flag & NNS_G3D_RSFLAG_OPT_RECORD)) {
                isUseRecordData = 1 ;
            } else {
                isUseRecordData = 0 ;
            }
        } else {
            isUseRecordData = 0 ;
            pAnmResult = &rs->tmpJntAnmResult;
        }
        if (!isUseRecordData) {
            pAnmResult->flag = (NNSG3dJntAnmResultFlag) 0;
            ((void) 0) ;
            if (rs->pRenderObj->anmJnt &&
                (*rs->pRenderObj->funcBlendJnt)(pAnmResult, rs->pRenderObj->anmJnt, idxNode)) {
                ;
            } else {
                const NNSG3dResNodeData * pNd =
                    NNS_G3dGetNodeDataByIdx(rs->pResNodeInfo, idxNode);
                const u8 * p = (const u8 *)pNd + sizeof(NNSG3dResNodeData);
                if (pNd->flag & NNS_G3D_SRTFLAG_TRANS_ZERO) {
                    pAnmResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO;
                } else {
                    const fx32 * p_fx32 = (const fx32 *)p;
                    pAnmResult->trans.x = *(p_fx32 + 0);
                    pAnmResult->trans.y = *(p_fx32 + 1);
                    pAnmResult->trans.z = *(p_fx32 + 2);
                    p += 3 * sizeof(fx32);
                }
                if (pNd->flag & NNS_G3D_SRTFLAG_ROT_ZERO) {
                    pAnmResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO;
                } else {
                    if (pNd->flag & NNS_G3D_SRTFLAG_PIVOT_EXIST) {
                        fx32 A = *(fx16 *)(p + 0);
                        fx32 B = *(fx16 *)(p + 2);
                        u32 idxPivot = (u32)((pNd->flag & NNS_G3D_SRTFLAG_IDXPIVOT_MASK) >>
                                             NNS_G3D_SRTFLAG_IDXPIVOT_SHIFT);
                        native_fn_02008f3c(&pAnmResult->rot);
                        pAnmResult->rot.a[idxPivot] =
                            (pNd->flag & NNS_G3D_SRTFLAG_PIVOT_MINUS) ?
                            -((fx32) 0x0000000000001000L) :
                            ((fx32) 0x0000000000001000L) ;
                        pAnmResult->rot.a[native_data_main_020d9068.field_0020[idxPivot][0]] = A;
                        pAnmResult->rot.a[native_data_main_020d9068.field_0020[idxPivot][1]] = B;
                        pAnmResult->rot.a[native_data_main_020d9068.field_0020[idxPivot][2]] =
                            (pNd->flag & NNS_G3D_SRTFLAG_SIGN_REVC) ? -B : B;
                        pAnmResult->rot.a[native_data_main_020d9068.field_0020[idxPivot][3]] =
                            (pNd->flag & NNS_G3D_SRTFLAG_SIGN_REVD) ? -A : A;
                        p += 2 * sizeof(fx16);
                    } else {
                        const fx16 * pp = (const fx16 *)p;
                        pAnmResult->rot.a[0] = pNd->_00;
                        pAnmResult->rot.a[1] = *(pp + 0);
                        pAnmResult->rot.a[2] = *(pp + 1);
                        pAnmResult->rot.a[3] = *(pp + 2);
                        pAnmResult->rot.a[4] = *(pp + 3);
                        pAnmResult->rot.a[5] = *(pp + 4);
                        pAnmResult->rot.a[6] = *(pp + 5);
                        pAnmResult->rot.a[7] = *(pp + 6);
                        pAnmResult->rot.a[8] = *(pp + 7);
                        p += 8 * sizeof(fx16);
                    }
                }
                ((void) 0) ;
                (*rs->funcJntScale)(pAnmResult, (fx32 *)p, rs->c, pNd->flag);
            }
        }
        rs->pJntAnmResult = pAnmResult;
    }
    cbFlag = NNSi_G3dCallBackCheck_B(rs, 0x06 , &cbTiming);
    if (!cbFlag) {
        if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD)) {
            ((void) 0) ;
            ((void) 0) ;
            (*rs->funcJntMtx)(rs->pJntAnmResult);
        }
    }
    rs->pJntAnmResult = ((void *)0) ;
    cbFlag = NNSi_G3dCallBackCheck_C(rs, 0x06 , cbTiming);
    if (opt == 0x20 ||
        opt == 0x60 ) {
        ++cmdLen;
        if (!cbFlag) {
            if (!(rs->flag & NNS_G3D_RSFLAG_OPT_NOGECMD)) {
                u32 idxMtxDest = *(rs->c + 4);
                ((void) 0) ;
                native_fn_0202e434(0x13 ,
                                    &idxMtxDest,
                                    1 );
            }
        }
    }
    rs->c += cmdLen;
}
