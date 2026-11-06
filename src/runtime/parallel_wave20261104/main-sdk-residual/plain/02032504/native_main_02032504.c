#include "context_00.h"
void native_main_02032504 (NNSG3dJntAnmResult * pResult)
{
    u32 idxNode;
    const NNSG3dResNodeData * pNd;
    const u8 * p;
    ((void) 0) ;
    ((void) 0) ;
    idxNode = *(native_data_main_020ee1f4->c + 1);
    pNd = NNS_G3dGetNodeDataByIdx(native_data_main_020ee1f4->pResNodeInfo, idxNode);
    p = (const u8 *)pNd + sizeof(*pNd);
    if (!(pNd->flag & NNS_G3D_SRTFLAG_TRANS_ZERO)) {
        p += 3 * sizeof(fx32);
    }
    if (!(pNd->flag & NNS_G3D_SRTFLAG_ROT_ZERO)) {
        if (pNd->flag & NNS_G3D_SRTFLAG_PIVOT_EXIST) {
            fx32 A = *(fx16 *)(p + 0);
            fx32 B = *(fx16 *)(p + sizeof(fx16));
            u32 idxPivot = (u32)((pNd->flag & NNS_G3D_SRTFLAG_IDXPIVOT_MASK) >>
                                 NNS_G3D_SRTFLAG_IDXPIVOT_SHIFT);
            native_fn_02008f3c(&pResult->rot);
            pResult->rot.a[idxPivot] =
                (pNd->flag & NNS_G3D_SRTFLAG_PIVOT_MINUS) ?
                -((fx32) 0x0000000000001000L) :
                ((fx32) 0x0000000000001000L) ;
            pResult->rot.a[native_data_main_020d90ac.field_0000[idxPivot][0]] = A;
            pResult->rot.a[native_data_main_020d90ac.field_0000[idxPivot][1]] = B;
            pResult->rot.a[native_data_main_020d90ac.field_0000[idxPivot][2]] =
                (pNd->flag & NNS_G3D_SRTFLAG_SIGN_REVC) ? -B : B;
            pResult->rot.a[native_data_main_020d90ac.field_0000[idxPivot][3]] =
                (pNd->flag & NNS_G3D_SRTFLAG_SIGN_REVD) ? -A : A;
        } else {
            const fx16 * pp = (const fx16 *)p;
            pResult->rot.a[0] = pNd->_00;
            pResult->rot.a[1] = *(pp + 0);
            pResult->rot.a[2] = *(pp + 1);
            pResult->rot.a[3] = *(pp + 2);
            pResult->rot.a[4] = *(pp + 3);
            pResult->rot.a[5] = *(pp + 4);
            pResult->rot.a[6] = *(pp + 5);
            pResult->rot.a[7] = *(pp + 6);
            pResult->rot.a[8] = *(pp + 7);
        }
    } else {
        pResult->flag |= NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO;
    }
}
