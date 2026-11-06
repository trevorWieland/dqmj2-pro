typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed long s32;
    typedef signed long long int s64;
        typedef int BOOL;
typedef s32 fx32;
    typedef union {
        struct {
            fx32 _00, _01;
            fx32 _10, _11;
        };
        fx32 m[2][2];
        fx32 a[4];
    } MtxFx22;
    typedef struct {
        union {
            u32 attr01;
            struct {
                u16 attr0;
                u16 attr1;
            };
            struct {
                u32 y : 8;
                u32 rsMode : 2;
                u32 objMode : 2;
                u32 mosaic : 1;
                u32 colorMode : 1;
                u32 shape : 2;
                u32 x : 9;
                u32 rsParam : 5;
                u32 size : 2;
            };
            struct {
                u32 _0 : 28;
                u32 flipH : 1;
                u32 flipV : 1;
                u32 _1 : 2;
            };
        };
        union {
            struct {
                u16 attr2;
                u16 _3;
            };
            u32 attr23;
            struct {
                u32 charNo : 10;
                u32 priority : 2;
                u32 cParam : 4;
                u32 _2 : 16;
            };
        };
    } GXOamAttr;
typedef enum {
    GX_OAM_SHAPE_8x8   = (0 << 14 ) | (0 << 30 ),
    GX_OAM_SHAPE_16x16 = (0 << 14 ) | (1 << 30 ),
    GX_OAM_SHAPE_32x32 = (0 << 14 ) | (2 << 30 ),
    GX_OAM_SHAPE_64x64 = (0 << 14 ) | (3 << 30 ),
    GX_OAM_SHAPE_16x8  = (1 << 14 ) | (0 << 30 ),
    GX_OAM_SHAPE_32x8  = (1 << 14 ) | (1 << 30 ),
    GX_OAM_SHAPE_32x16 = (1 << 14 ) | (2 << 30 ),
    GX_OAM_SHAPE_64x32 = (1 << 14 ) | (3 << 30 ),
    GX_OAM_SHAPE_8x16  = (2 << 14 ) | (0 << 30 ),
    GX_OAM_SHAPE_8x32  = (2 << 14 ) | (1 << 30 ),
    GX_OAM_SHAPE_16x32 = (2 << 14 ) | (2 << 30 ),
    GX_OAM_SHAPE_32x64 = (2 << 14 ) | (3 << 30 )
} GXOamShape;
typedef enum {
    GX_OAM_EFFECT_NONE          = (0 << 8 ) | (0 << 28 ) | (0 << 29 ),
    GX_OAM_EFFECT_FLIP_H        = (0 << 8 ) | (1 << 28 ) | (0 << 29 ),
    GX_OAM_EFFECT_FLIP_V        = (0 << 8 ) | (0 << 28 ) | (1 << 29 ),
    GX_OAM_EFFECT_FLIP_HV       = (0 << 8 ) | (1 << 28 ) | (1 << 29 ),
    GX_OAM_EFFECT_AFFINE        = (1 << 8 ),
    GX_OAM_EFFECT_NODISPLAY     = (2 << 8 ),
    GX_OAM_EFFECT_AFFINE_DOUBLE = (3 << 8 )
} GXOamEffect;
static void G2_SetOBJPosition(GXOamAttr * oam, int x, int y);
static void G2_SetOBJEffect(GXOamAttr * oam, GXOamEffect effect, int rsParam);
static inline void G2_SetOBJPosition (GXOamAttr * oam, int x, int y)
{
    oam->attr01 = ((oam->attr01 & ~(0x000000ff | 0x01ff0000 )) |
                   (y & 0x000000ff ) |
                   ((x & (0x01ff0000 >> 16 )) <<
                    16 ));
}
static inline void G2_SetOBJEffect (GXOamAttr * oam, GXOamEffect effect, int rsParam)
{
    if (GX_OAM_EFFECT_AFFINE != effect && GX_OAM_EFFECT_AFFINE_DOUBLE != effect) {
        oam->attr01 = ((oam->attr01 & ~(0x00000300 | 0x3e000000 )) |
                       effect);
    } else {
        oam->attr01 = ((oam->attr01 & ~(0x00000300 | 0x3e000000 )) |
                       effect | (rsParam << 25 ));
    }
}
static inline GXOamEffect G2_GetOBJEffect (const GXOamAttr * oam)
{
    GXOamEffect effect;
    effect = (GXOamEffect)(oam->attr01 & 0x00000300 );
    if (effect == GX_OAM_EFFECT_AFFINE || effect == GX_OAM_EFFECT_AFFINE_DOUBLE) {
        return effect;
    }
    return (GXOamEffect)(effect | (oam->attr01 & 0x30000000 ));
}
typedef struct NNSG2dFVec2 {
    fx32 x;
    fx32 y;
} NNSG2dFVec2;
typedef struct NNSG2dCellOAMAttrData {
    u16 attr0;
    u16 attr1;
    u16 attr2;
} NNSG2dCellOAMAttrData;
typedef struct NNSG2dCellData {
    u16 numOAMAttrs;
    u16 cellAttr;
    NNSG2dCellOAMAttrData * pOamAttrArray;
} NNSG2dCellData;
inline void NNS_G2dCopyCellAsOamAttr (const NNSG2dCellData * pCell, u16 idx, GXOamAttr * pDst)
{
    {
        const NNSG2dCellOAMAttrData * pSrc = pCell->pOamAttrArray + idx;
        pDst->attr0 = pSrc->attr0;
        pDst->attr1 = pSrc->attr1;
        pDst->attr2 = pSrc->attr2;
    }
}
inline s16 NNS_G2dRepeatXinCellSpace (s16 srcX)
{
    if (srcX > 255 ) {
        srcX |= 0xFF00;
    }
    return srcX;
}
inline s16 NNS_G2dRepeatYinCellSpace (s16 srcY)
{
    if (srcY > 127 ) {
        srcY |= 0xFF00;
    }
    return srcY;
}
    extern const u16 native_data_020d9170[3][4];
    extern const u16 native_data_020d9188[3][4];
inline GXOamShape NNS_G2dGetOAMSize (const GXOamAttr * oamAttr)
{
    const GXOamShape result = (GXOamShape)((0x0000c000 | 0xc0000000 ) & oamAttr->attr01);
    return result;
}
inline int NNS_G2dGetOamSizeX (const GXOamShape * oamShape)
{
    return native_data_020d9188[(*oamShape & 0x0000c000 ) >> 14 ]
           [(*oamShape & 0xc0000000 ) >> 30 ];
}
inline int NNS_G2dGetOamSizeY (const GXOamShape * oamShape)
{
    return native_data_020d9170[(*oamShape & 0x0000c000 ) >> 14 ]
           [(*oamShape & 0xc0000000 ) >> 30 ];
}
u16 native_main_0203519c(GXOamAttr * pDstOams, u16 numDstOam, const NNSG2dCellData * pCell, const MtxFx22 * pMtxSR, const NNSG2dFVec2 * pBaseTrans, u16 affineIndex, BOOL bDoubleAffine);
static s16 NNSi_G2dGetOamX(const GXOamAttr * oamAttr);
static s16 NNSi_G2dGetOamY(const GXOamAttr * oamAttr);
static void NNSi_G2dAdjustDifferenceOfRotateOrientation(const GXOamAttr * pOam, const MtxFx22 * pM, NNSG2dFVec2 * pV, BOOL adjustDoubleAffine);
inline s16 NNSi_G2dGetOamX (const GXOamAttr * oamAttr)
{
    {
        s16 val = (s16)((0x01ff0000 & oamAttr->attr01) >> 16 );
        return val;
    }
}
inline s16 NNSi_G2dGetOamY (const GXOamAttr * oamAttr)
{
    {
        s16 val = (s16)((0x000000ff & oamAttr->attr01) >> 0 );
        return val;
    }
}
inline void NNS_G2dGetOamTransFx32 (const GXOamAttr * pOam, NNSG2dFVec2 * pRet)
{
    pRet->x = (fx32)(NNS_G2dRepeatXinCellSpace(NNSi_G2dGetOamX(pOam)) * ((fx32) 0x0000000000001000L) );
    pRet->y = (fx32)(NNS_G2dRepeatYinCellSpace(NNSi_G2dGetOamY(pOam)) * ((fx32) 0x0000000000001000L) );
}
inline void NNSi_G2dRemovePositionAdjustmentFromDoubleAffineOBJ (const GXOamAttr * pOam, NNSG2dFVec2 * pV)
{
    if (G2_GetOBJEffect(pOam) == GX_OAM_EFFECT_AFFINE_DOUBLE) {
        const GXOamShape oamShape = NNS_G2dGetOAMSize(pOam);
        const int halfW = NNS_G2dGetOamSizeX(&oamShape) << (12 - 1);
        const int halfH = NNS_G2dGetOamSizeY(&oamShape) << (12 - 1);
        pV->x += halfW;
        pV->y += halfH;
    }
}
inline void NNSi_G2dAdjustDifferenceOfRotateOrientation (const GXOamAttr * pOam, const MtxFx22 * pM, NNSG2dFVec2 * pV, BOOL adjustDoubleAffine)
{
    {
        const GXOamShape oamShape = NNS_G2dGetOAMSize(pOam);
        const int halfW = NNS_G2dGetOamSizeX(&oamShape) >> 1;
        const int halfH = NNS_G2dGetOamSizeY(&oamShape) >> 1;
        pV->x += -(halfW << 12 ) + pM->_00 * halfW + pM->_10 * halfH;
        pV->y += -(halfH << 12 ) + pM->_01 * halfW + pM->_11 * halfH;
        if (adjustDoubleAffine) {
            pV->x -= halfW << 12 ;
            pV->y -= halfH << 12 ;
        }
    }
}
inline void MulMtx22 (const MtxFx22 * m, const NNSG2dFVec2 * pSrc, NNSG2dFVec2 * pDst)
{
    NNSG2dFVec2 temp;
    NNSG2dFVec2 * pV = pDst;
    if (pDst == pSrc) {
        pV = &temp;
    }
    pV->x = (fx32)((((s64) (m->_00) * pSrc->x + 0x800LL)
                    + ((s64) (m->_10) * pSrc->y + 0x800LL)) >> 12 );
    pV->y = (fx32)((((s64) (m->_01) * pSrc->x + 0x800LL)
                    + ((s64) (m->_11) * pSrc->y + 0x800LL)) >> 12 );
    if (pV == &temp) {
        *pDst = temp;
    }
}
u16 native_main_0203519c (GXOamAttr * pDstOams, u16 numDstOam, const NNSG2dCellData * pCell, const MtxFx22 * pMtxSR, const NNSG2dFVec2 * pBaseTrans, u16 affineIndex, BOOL bDoubleAffine)
{
    u16 i = 0;
    NNSG2dFVec2 objTrans;
    GXOamAttr * pDstOam = ((void *)0) ;
    const u16 numOBJ
        = (numDstOam < pCell->numOAMAttrs) ? numDstOam : pCell->numOAMAttrs;
    for (i = 0; i < numOBJ; i++) {
        pDstOam = &pDstOams[i];
        NNS_G2dCopyCellAsOamAttr(pCell, i, pDstOam);
        if ( pMtxSR != ((void *)0) || pBaseTrans != ((void *)0) ) {
            NNS_G2dGetOamTransFx32(pDstOam, &objTrans);
            if ( pMtxSR != ((void *)0) ) {
                NNSi_G2dRemovePositionAdjustmentFromDoubleAffineOBJ(pDstOam, &objTrans);
                {
                    const GXOamEffect effectTypeAfter = (bDoubleAffine) ?
                                                        GX_OAM_EFFECT_AFFINE_DOUBLE : GX_OAM_EFFECT_AFFINE;
                    const BOOL bShouldAdjust = (effectTypeAfter  == GX_OAM_EFFECT_AFFINE_DOUBLE);
                    MulMtx22(pMtxSR, &objTrans, &objTrans);
                    G2_SetOBJEffect(pDstOam, effectTypeAfter, affineIndex);
                    NNSi_G2dAdjustDifferenceOfRotateOrientation(pDstOam,
                                                                pMtxSR,
                                                                &objTrans,
                                                                bShouldAdjust);
                }
            }
            if ( pBaseTrans != ((void *)0) ) {
                objTrans.x += pBaseTrans->x;
                objTrans.y += pBaseTrans->y;
            }
            G2_SetOBJPosition(pDstOam,
                              (objTrans.x + 0x800) >> 12 ,
                              (objTrans.y + 0x800) >> 12 );
        }
    }
    return numOBJ;
}
