#include "context.h"
void native_main_02030f58 (NNSG3dRS * rs, u32)
{
    fx64 w = 0;
    const NNSG3dResEvpMtx * evpMtx =
        (const NNSG3dResEvpMtx *)((u8 *)rs->pRenderObj->resMdl +
                                  rs->pRenderObj->resMdl->ofsEvpMtx);
    u32 numMtx = *(rs->c + 2);
    u8 * p = rs->c + 3;
    ((void) 0) ;
    {
        u32 i;
        struct {
            MtxFx43 M;
            MtxFx33 N;
        } sum;
        MtxFx44 * pX;
        MtxFx33 * pY;
        MI_CpuClearFast(&sum, sizeof(sum));
        native_fn_0202e300();
        G3_MtxMode(GX_MTXMODE_PROJECTION);
        G3_StoreMtx(1);
        G3_Identity();
        G3_MtxMode(GX_MTXMODE_POSITION_VECTOR);
        for (i = 0; i < numMtx; ++i) {
            u32 idxJnt = *(p + 1);
            BOOL evpCached = NNSi_G3dBitVecCheck(&rs->isEvpCached[0], idxJnt);
            pX = &native_data_020ee1f8.evpCache[idxJnt].M;
            if (!evpCached) {
                NNSi_G3dBitVecSet(&rs->isEvpCached[0], idxJnt);
                G3_RestoreMtx(*p);
                G3_MtxMode(GX_MTXMODE_POSITION);
                native_fn_02004368((u32)&evpMtx[idxJnt].invM);
            }
            if (i != 0) {
                sum.N.m[0][0] += (w * pY->m[0][0]) >> 12 ;
                sum.N.m[0][1] += (w * pY->m[0][1]) >> 12 ;
                sum.N.m[0][2] += (w * pY->m[0][2]) >> 12 ;
                sum.N.m[1][0] += (w * pY->m[1][0]) >> 12 ;
                sum.N.m[1][1] += (w * pY->m[1][1]) >> 12 ;
                sum.N.m[1][2] += (w * pY->m[1][2]) >> 12 ;
                sum.N.m[2][0] += (w * pY->m[2][0]) >> 12 ;
                sum.N.m[2][1] += (w * pY->m[2][1]) >> 12 ;
                sum.N.m[2][2] += (w * pY->m[2][2]) >> 12 ;
            }
            if (!evpCached) {
                while (native_fn_02004668(pX))
                    ;
                G3_MtxMode(GX_MTXMODE_POSITION_VECTOR);
                native_fn_02004384((u32)&evpMtx[idxJnt].invN);
            }
            w = *(p + 2) << 4;
            sum.M.m[0][0] += (w * pX->m[0][0]) >> 12 ;
            sum.M.m[0][1] += (w * pX->m[0][1]) >> 12 ;
            sum.M.m[0][2] += (w * pX->m[0][2]) >> 12 ;
            sum.M.m[1][0] += (w * pX->m[1][0]) >> 12 ;
            sum.M.m[1][1] += (w * pX->m[1][1]) >> 12 ;
            sum.M.m[1][2] += (w * pX->m[1][2]) >> 12 ;
            sum.M.m[2][0] += (w * pX->m[2][0]) >> 12 ;
            sum.M.m[2][1] += (w * pX->m[2][1]) >> 12 ;
            sum.M.m[2][2] += (w * pX->m[2][2]) >> 12 ;
            sum.M.m[3][0] += (w * pX->m[3][0]) >> 12 ;
            sum.M.m[3][1] += (w * pX->m[3][1]) >> 12 ;
            sum.M.m[3][2] += (w * pX->m[3][2]) >> 12 ;
            p += 3;
            pY = &native_data_020ee1f8.evpCache[idxJnt].N;
            if (!evpCached) {
                while (native_fn_02004698(pY))
                    ;
            }
        }
        sum.N.m[0][0] += (w * pY->m[0][0]) >> 12 ;
        sum.N.m[0][1] += (w * pY->m[0][1]) >> 12 ;
        sum.N.m[0][2] += (w * pY->m[0][2]) >> 12 ;
        sum.N.m[1][0] += (w * pY->m[1][0]) >> 12 ;
        sum.N.m[1][1] += (w * pY->m[1][1]) >> 12 ;
        sum.N.m[1][2] += (w * pY->m[1][2]) >> 12 ;
        sum.N.m[2][0] += (w * pY->m[2][0]) >> 12 ;
        sum.N.m[2][1] += (w * pY->m[2][1]) >> 12 ;
        sum.N.m[2][2] += (w * pY->m[2][2]) >> 12 ;
        native_fn_0200434c((u32)&sum.N);
        G3_MtxMode(GX_MTXMODE_POSITION);
        native_fn_0200434c((u32)&sum.M);
        G3_MtxMode(GX_MTXMODE_PROJECTION);
        G3_RestoreMtx(1);
        G3_MtxMode(GX_MTXMODE_POSITION_VECTOR);
    }
    G3_StoreMtx(*(rs->c + 1));
    rs->c += 3 + *(rs->c + 2) * 3;
}
