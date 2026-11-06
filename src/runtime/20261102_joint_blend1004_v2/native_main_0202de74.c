typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed int s32;
    typedef signed long long int s64;
        typedef int BOOL;
void native_fn_02008c28(const void * srcp, void * destp, u32 size);
void native_fn_02008c58(u32 data, void * destp, u32 size);
static inline void MI_CpuCopy32 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c28(src, dest, size);
}
static inline void MI_CpuFillFast (void * dest, u32 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c58(data, dest, size);
}
static inline void MI_CpuClearFast (void * dest, u32 size)
{
	MI_CpuFillFast(dest, 0, size);
}
typedef s32 fx32;
typedef s64 fx64;
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
extern const u16 (*ctrdgi_fl_maxtime);
u32 native_fn_0200235c(u32 numer, s32 denom);
void native_fn_02002534(const VecFx32 * a, const VecFx32 * b, VecFx32 * axb);
void native_fn_02002618(const VecFx32 * pSrc, VecFx32 * pDst);
typedef u32 NNSGfdTexKey;
typedef struct NNSG3dResDataBlockHeader_ {
    union {
        u32 kind;
        char chr[4];
    };
    u32 size;
} NNSG3dResDataBlockHeader;
typedef struct NNSG3dResDictTreeNode_ {
    u8 refBit;
    u8 idxLeft;
    u8 idxRight;
    u8 idxEntry;
} NNSG3dResDictTreeNode;
typedef struct NNSG3dResDict_ {
    u8 revision;
    u8 numEntry;
    u16 sizeDictBlk;
    u16 dummy_;
    u16 ofsEntry;
    NNSG3dResDictTreeNode node[1];
} NNSG3dResDict;
typedef struct NNSG3dResTexInfo_ {
    NNSGfdTexKey vramKey;
    u16 sizeTex;
    u16 ofsDict;
    u16 flag;
    u16 dummy_;
    u32 ofsTex;
} NNSG3dResTexInfo;
typedef struct NNSG3dResTex4x4Info_ {
    NNSGfdTexKey vramKey;
    u16 sizeTex;
    u16 ofsDict;
    u16 flag;
    u16 dummy_;
    u32 ofsTex;
    u32 ofsTexPlttIdx;
} NNSG3dResTex4x4Info;
typedef struct NNSG3dResPlttInfo_ {
    NNSGfdTexKey vramKey;
    u16 sizePltt;
    u16 flag;
    u16 ofsDict;
    u16 dummy_;
    u32 ofsPlttData;
} NNSG3dResPlttInfo;
typedef struct NNSG3dResTex_ {
    NNSG3dResDataBlockHeader header;
    NNSG3dResTexInfo texInfo;
    NNSG3dResTex4x4Info tex4x4Info;
    NNSG3dResPlttInfo plttInfo;
    NNSG3dResDict dict;
} NNSG3dResTex;
typedef struct NNSG3dAnmObj_ {
    fx32 frame;
    fx32 ratio;
    void * resAnm;
    void * funcAnm;
    struct NNSG3dAnmObj_ * next;
    const NNSG3dResTex * resTex;
    u8 priority;
    u8 numMapData;
    u16 mapData[1];
} NNSG3dAnmObj;
typedef enum {
    NNS_G3D_ANMOBJ_MAPDATA_EXIST     = 0x0100,
    NNS_G3D_ANMOBJ_MAPDATA_DISABLED  = 0x0200,
    NNS_G3D_ANMOBJ_MAPDATA_DATAFIELD = 0x00ff
} NNSG3dAnmObjMapData;
struct NNSG3dJntAnmResult_;
typedef enum {
    NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE    = 0x00000001,
    NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO     = 0x00000002,
    NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO   = 0x00000004,
    NNS_G3D_JNTANM_RESULTFLAG_SCALEEX0_ONE = 0x00000008,
    NNS_G3D_JNTANM_RESULTFLAG_SCALEEX1_ONE = 0x00000010,
    NNS_G3D_JNTANM_RESULTFLAG_MAYA_SSC     = 0x00000020
} NNSG3dJntAnmResultFlag;
typedef struct NNSG3dJntAnmResult_ {
    NNSG3dJntAnmResultFlag flag;
    VecFx32 scale;
    VecFx32 scaleEx0;
    VecFx32 scaleEx1;
    MtxFx33 rot;
    VecFx32 trans;
} NNSG3dJntAnmResult;
typedef void (*NNSG3dFuncAnmJnt)(NNSG3dJntAnmResult *, const NNSG3dAnmObj *, u32);
BOOL native_main_0202de74(NNSG3dJntAnmResult *, const NNSG3dAnmObj *, u32);
u32 native_fn_0202de04 (void * v0, void * v1, s32 ratio, s32 isV1One);
BOOL native_main_0202de74 (NNSG3dJntAnmResult * pResult, const NNSG3dAnmObj * pAnmObj, u32 nodeID)
{
    ((void) 0) ;
    if (!pAnmObj) {
        return 0 ;
    }
    if (!pAnmObj->next) {
        u32 dataIdx;
        if (nodeID < pAnmObj->numMapData) {
            dataIdx = pAnmObj->mapData[nodeID];
            if ((dataIdx & (NNS_G3D_ANMOBJ_MAPDATA_EXIST |
                            NNS_G3D_ANMOBJ_MAPDATA_DISABLED)) ==
                NNS_G3D_ANMOBJ_MAPDATA_EXIST) {
                NNSG3dFuncAnmJnt func = (NNSG3dFuncAnmJnt)pAnmObj->funcAnm;
                ((void) 0) ;
                if (func) {
                    (*func)(pResult,
                            pAnmObj,
                            dataIdx & NNS_G3D_ANMOBJ_MAPDATA_DATAFIELD);
                    return 1 ;
                } else {
                    return 0 ;
                }
            } else {
                return 0 ;
            }
        } else {
            return 0 ;
        }
    } else {
        const NNSG3dAnmObj * p;
        NNSG3dJntAnmResult r;
        fx32 sumOfRatio = 0;
        const NNSG3dAnmObj * pLastAnmObj;
        int numBlend = 0;
        int i1 = 0;
        VecFx32 keepAxisX;
        VecFx32 keepAxisZ;
        p = pAnmObj;
        do {
            if (nodeID < p->numMapData) {
                u32 dataIdx = p->mapData[nodeID];
                if ((dataIdx & (NNS_G3D_ANMOBJ_MAPDATA_EXIST |
                                NNS_G3D_ANMOBJ_MAPDATA_DISABLED)) ==
                    NNS_G3D_ANMOBJ_MAPDATA_EXIST) {
                    ((void) 0) ;
                    if (p->ratio > ((fx32) 0x0000000000001000L) )
                        sumOfRatio += ((fx32) 0x0000000000001000L) ;
                    else if (p->ratio > 0)
                        sumOfRatio += p->ratio;
                    pLastAnmObj = p;
                    ++numBlend;
                }
            }
            p = p->next;
        } while (p);
        if (sumOfRatio == 0) {
            return 0 ;
        }
        if (numBlend == 1) {
            NNSG3dFuncAnmJnt func = (NNSG3dFuncAnmJnt)pLastAnmObj->funcAnm;
            u32 dataIdx = pLastAnmObj->mapData[nodeID];
            ((void) 0) ;
            if (func) {
                (*func)(pResult, pLastAnmObj, dataIdx & NNS_G3D_ANMOBJ_MAPDATA_DATAFIELD);
                return 1 ;
            } else {
                return 0 ;
            }
        }
        MI_CpuClearFast(pResult, sizeof(*pResult));
        pResult->flag = (NNSG3dJntAnmResultFlag) - 1;
        p = pAnmObj;
        do {
            if (nodeID < p->numMapData) {
                u32 dataIdx = p->mapData[nodeID];
                if ((dataIdx & (NNS_G3D_ANMOBJ_MAPDATA_EXIST |
                                NNS_G3D_ANMOBJ_MAPDATA_DISABLED)) ==
                    NNS_G3D_ANMOBJ_MAPDATA_EXIST &&
                    (p->ratio > 0)) {
                    fx32 ratio;
                    NNSG3dFuncAnmJnt func = (NNSG3dFuncAnmJnt)p->funcAnm;
                    ((void) 0) ;
                    if (func) {
                        (*func)(&r, p, dataIdx & NNS_G3D_ANMOBJ_MAPDATA_DATAFIELD);
                        if (i1 == 0) {
                            MI_CpuCopy32(&r.rot._00, &keepAxisX, sizeof(VecFx32));
                            MI_CpuCopy32(&r.rot._20, &keepAxisZ, sizeof(VecFx32));
                        }
                        if (sumOfRatio != ((fx32) 0x0000000000001000L) ) {
                            ratio = (fx32)native_fn_0200235c((u32)p->ratio, sumOfRatio);
                        } else {
                            ratio = p->ratio;
                        }
                        native_fn_0202de04(&pResult->scale,
                                       &r.scale,
                                       ratio,
                                       r.flag & NNS_G3D_JNTANM_RESULTFLAG_SCALE_ONE);
                        native_fn_0202de04(&pResult->scaleEx0,
                                       &r.scaleEx0,
                                       ratio,
                                       r.flag & NNS_G3D_JNTANM_RESULTFLAG_SCALEEX0_ONE);
                        native_fn_0202de04(&pResult->scaleEx1,
                                       &r.scaleEx1,
                                       ratio,
                                       r.flag & NNS_G3D_JNTANM_RESULTFLAG_SCALEEX1_ONE);
                        if (!(r.flag & NNS_G3D_JNTANM_RESULTFLAG_TRANS_ZERO)) {
                            pResult->trans.x += (fx32)((fx64)ratio * r.trans.x >> 12 );
                            pResult->trans.y += (fx32)((fx64)ratio * r.trans.y >> 12 );
                            pResult->trans.z += (fx32)((fx64)ratio * r.trans.z >> 12 );
                        }
                        if (!(r.flag & NNS_G3D_JNTANM_RESULTFLAG_ROT_ZERO)) {
                            pResult->rot._00 += ratio * r.rot._00 >> 12 ;
                            pResult->rot._01 += ratio * r.rot._01 >> 12 ;
                            pResult->rot._02 += ratio * r.rot._02 >> 12 ;
                            pResult->rot._10 += ratio * r.rot._10 >> 12 ;
                            pResult->rot._11 += ratio * r.rot._11 >> 12 ;
                            pResult->rot._12 += ratio * r.rot._12 >> 12 ;
                        } else {
                            pResult->rot._00 += ratio;
                            pResult->rot._11 += ratio;
                        }
                        pResult->flag &= r.flag;
                    }
                }
            }
            p = p->next;
            ++i1;
        } while (p);
        native_fn_02002534((VecFx32 *)&pResult->rot._00,
                         (VecFx32 *)&pResult->rot._10,
                         (VecFx32 *)&pResult->rot._20);
        if ((pResult->rot._00 == 0) &&
            (pResult->rot._01 == 0) &&
            (pResult->rot._02 == 0)) {
            MI_CpuCopy32(&keepAxisX, &pResult->rot._00, sizeof(VecFx32));
        } else {
            native_fn_02002618((VecFx32 *)&pResult->rot._00, (VecFx32 *)&pResult->rot._00);
        }
        if ((pResult->rot._20 == 0) &&
            (pResult->rot._21 == 0) &&
            (pResult->rot._22 == 0)) {
            MI_CpuCopy32(&keepAxisZ, &pResult->rot._20, sizeof(VecFx32));
        } else {
            native_fn_02002618((VecFx32 *)&pResult->rot._20, (VecFx32 *)&pResult->rot._20);
        }
        native_fn_02002534((VecFx32 *)&pResult->rot._20,
                         (VecFx32 *)&pResult->rot._00,
                         (VecFx32 *)&pResult->rot._10);
        return 1 ;
    }
}
