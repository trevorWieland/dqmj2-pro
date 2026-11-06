typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed int s32;
        typedef int BOOL;
typedef s32 fx32;
typedef struct {
    fx32 x;
    fx32 y;
    fx32 z;
} VecFx32;
    typedef union {
        struct {
            fx32 _00, _01, _02;
            fx32 _10, _11, _12;
            fx32 _20, _21, _22;
        };
        fx32 m[3][3];
        fx32 a[9];
    } MtxFx33;
    static s32 FX_Whole(fx32 v);
    static inline s32 FX_Whole (fx32 v)
    {
        return (s32)(v >> 12 );
    }
extern const u16 (*ctrdgi_fl_maxtime);
void native_fn_02002618(const VecFx32 * pSrc, VecFx32 * pDst);
typedef struct NNSG3dResAnmHeader_ {
    u8 category0;
    u8 revision;
    u16 category1;
} NNSG3dResAnmHeader;
typedef enum {
    NNS_G3D_JNTANM_RINFO_STEP_1            = 0x00000000,
    NNS_G3D_JNTANM_RINFO_STEP_2            = 0x40000000,
    NNS_G3D_JNTANM_RINFO_STEP_4            = 0x80000000,
    NNS_G3D_JNTANM_RINFO_LAST_INTERP_MASK  = 0x1fff0000,
    NNS_G3D_JNTANM_RINFO_STEP_MASK         = 0xc0000000,
    NNS_G3D_JNTANM_RINFO_LAST_INTERP_SHIFT = 16,
    NNS_G3D_JNTANM_RINFO_STEP_SHIFT        = 30
} NNSG3dJntAnmRInfo;
typedef enum {
    NNS_G3D_JNTANM_RIDX_PIVOT         = 0x8000,
    NNS_G3D_JNTANM_RIDX_IDXDATA_MASK  = 0x7fff,
    NNS_G3D_JNTANM_RIDX_IDXDATA_SHIFT = 0
} NNSG3dJntAnmRIdx;
typedef struct NNSG3dResJntAnm_ {
    NNSG3dResAnmHeader anmHeader;
    u16 numFrame;
    u16 numNode;
    u32 flag;
    u32 ofsRot3;
    u32 ofsRot5;
} NNSG3dResJntAnm;
void native_main_02033068(MtxFx33 * pRot, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm);
static BOOL native_fn_020337c4(MtxFx33 * pRot, const void * pArrayRot3, const void * pArrayRot5, NNSG3dJntAnmRIdx info);
static inline void vecCross_ (const VecFx32 * a, const VecFx32 * b, VecFx32 * axb)
{
    fx32 x, y, z;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    x = (a->y * b->z - a->z * b->y) >> 12 ;
    y = (a->z * b->x - a->x * b->z) >> 12 ;
    z = (a->x * b->y - a->y * b->x) >> 12 ;
    axb->x = x;
    axb->y = y;
    axb->z = z;
}
void native_main_02033068 (MtxFx33 * pRot, fx32 Frame, const u32 * pData, const NNSG3dResJntAnm * pJntAnm)
{
    u32 frame = (u32)FX_Whole(Frame);
    const void * pArray = (const void *)((const u8 *)pJntAnm + *(pData + 1));
    const void * pArrayRot3 = (const void *)((const u8 *)pJntAnm + pJntAnm->ofsRot3);
    const void * pArrayRot5 = (const void *)((const u8 *)pJntAnm + pJntAnm->ofsRot5);
    NNSG3dJntAnmRInfo info = (NNSG3dJntAnmRInfo) * pData;
    const u16 * p = (const u16 *)pArray;
    u32 last_interp;
    u32 idx;
    u32 idx_sub;
    if (!(info & NNS_G3D_JNTANM_RINFO_STEP_MASK)) {
        idx = frame;
        goto ROT_NONINTERP;
    }
    last_interp = ((u32)info & NNS_G3D_JNTANM_RINFO_LAST_INTERP_MASK) >>
                  NNS_G3D_JNTANM_RINFO_LAST_INTERP_SHIFT;
    if (info & NNS_G3D_JNTANM_RINFO_STEP_2) {
        if (frame & 1) {
            if (frame > last_interp) {
                idx = (last_interp >> 1) + 1;
                goto ROT_NONINTERP;
            } else {
                idx = frame >> 1;
                goto ROT_INTERP_2;
            }
        } else {
            idx = frame >> 1;
            goto ROT_NONINTERP;
        }
    } else {
        if (frame & 3) {
            if (frame > last_interp) {
                idx = (last_interp >> 2) + (frame & 3);
                goto ROT_NONINTERP;
            }
            if (frame & 1) {
                MtxFx33 tmp;
                BOOL doCross = 0 ;
                if (frame & 2) {
                    idx_sub = (frame >> 2);
                    idx = idx_sub + 1;
                } else {
                    idx = (frame >> 2);
                    idx_sub = idx + 1;
                }
                doCross |= native_fn_020337c4(pRot,
                                            pArrayRot3,
                                            pArrayRot5,
                                            (NNSG3dJntAnmRIdx)p[idx]);
                doCross |= native_fn_020337c4(&tmp,
                                            pArrayRot3,
                                            pArrayRot5,
                                            (NNSG3dJntAnmRIdx)p[idx_sub]);
                pRot->_00 = (pRot->_00 * 3 + tmp._00) >> (2 * 0 );
                pRot->_01 = (pRot->_01 * 3 + tmp._01) >> (2 * 0 );
                pRot->_02 = (pRot->_02 * 3 + tmp._02) >> (2 * 0 );
                pRot->_10 = (pRot->_10 * 3 + tmp._10) >> (2 * 0 );
                pRot->_11 = (pRot->_11 * 3 + tmp._11) >> (2 * 0 );
                pRot->_12 = (pRot->_12 * 3 + tmp._12) >> (2 * 0 );
                native_fn_02002618((VecFx32 *)(&pRot->_00), (VecFx32 *)(&pRot->_00));
                native_fn_02002618((VecFx32 *)(&pRot->_10), (VecFx32 *)(&pRot->_10));
                if (!doCross) {
                    pRot->_20 = (pRot->_20 * 3 + tmp._20) >> (2 * 0 );
                    pRot->_21 = (pRot->_21 * 3 + tmp._21) >> (2 * 0 );
                    pRot->_22 = (pRot->_22 * 3 + tmp._22) >> (2 * 0 );
                    native_fn_02002618((VecFx32 *)(&pRot->_20), (VecFx32 *)(&pRot->_20));
                } else {
                    vecCross_((const VecFx32 *)&pRot->_00,
                              (const VecFx32 *)&pRot->_10,
                              (VecFx32 *)&pRot->_20);
                }
                return;
            } else {
                idx = frame >> 2;
                goto ROT_INTERP_2;
            }
        } else {
            idx = frame >> 2;
            goto ROT_NONINTERP;
        }
    }
ROT_INTERP_2:
    {
        MtxFx33 tmp;
        BOOL doCross = 0 ;
        doCross |= native_fn_020337c4(pRot,
                                    pArrayRot3,
                                    pArrayRot5,
                                    (NNSG3dJntAnmRIdx)p[idx]);
        doCross |= native_fn_020337c4(&tmp,
                                    pArrayRot3,
                                    pArrayRot5,
                                    (NNSG3dJntAnmRIdx)p[idx + 1]);
        pRot->_00 = (pRot->_00 + tmp._00) >> 0 ;
        pRot->_01 = (pRot->_01 + tmp._01) >> 0 ;
        pRot->_02 = (pRot->_02 + tmp._02) >> 0 ;
        pRot->_10 = (pRot->_10 + tmp._10) >> 0 ;
        pRot->_11 = (pRot->_11 + tmp._11) >> 0 ;
        pRot->_12 = (pRot->_12 + tmp._12) >> 0 ;
        native_fn_02002618((VecFx32 *)(&pRot->_00), (VecFx32 *)(&pRot->_00));
        native_fn_02002618((VecFx32 *)(&pRot->_10), (VecFx32 *)(&pRot->_10));
        if (!doCross) {
            pRot->_20 = (pRot->_20 + tmp._20) >> 0 ;
            pRot->_21 = (pRot->_21 + tmp._21) >> 0 ;
            pRot->_22 = (pRot->_22 + tmp._22) >> 0 ;
            native_fn_02002618((VecFx32 *)(&pRot->_20), (VecFx32 *)(&pRot->_20));
        } else {
            vecCross_((const VecFx32 *)&pRot->_00,
                      (const VecFx32 *)&pRot->_10,
                      (VecFx32 *)&pRot->_20);
        }
        return;
    }
ROT_NONINTERP:
    if (native_fn_020337c4(pRot,
                         pArrayRot3,
                         pArrayRot5,
                         (NNSG3dJntAnmRIdx)p[idx])) {
        vecCross_((const VecFx32 *)&pRot->_00,
                  (const VecFx32 *)&pRot->_10,
                  (VecFx32 *)&pRot->_20);
    } else {
        native_fn_02002618((VecFx32 *)(&pRot->_20), (VecFx32 *)(&pRot->_20));
    }
    return;
}
BOOL native_fn_020337c4 (MtxFx33 * pRot, const void * pArrayRot3, const void * pArrayRot5, NNSG3dJntAnmRIdx info);

typedef char checked_u32_width[(sizeof(u32)==4)?1:-1];
