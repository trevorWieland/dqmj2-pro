typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed long s32;
typedef signed long long int s64;
typedef int BOOL;
void native_fn_02008c28(const void * srcp, void * destp, u32 size);
typedef s32 fx32;
typedef s64 fx64;
typedef s16 fx16;
typedef struct {
    fx32 x;
    fx32 y;
    fx32 z;
} VecFx32;
typedef union {
        struct {
            fx32 _00, _01, _02, _03;
            fx32 _10, _11, _12, _13;
            fx32 _20, _21, _22, _23;
            fx32 _30, _31, _32, _33;
        };
        fx32 m[4][4];
        fx32 a[16];
    } MtxFx44;
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
typedef struct NNSG3dResMat_ {
    u16 ofsDictTexToMatList;
    u16 ofsDictPlttToMatList;
    NNSG3dResDict dict;
} NNSG3dResMat;
typedef struct NNSG3dResShp_ {
    NNSG3dResDict dict;
} NNSG3dResShp;
typedef struct NNSG3dResMdlInfo_ {
    u8 sbcType;
    u8 scalingRule;
    u8 texMtxMode;
    u8 numNode;
    u8 numMat;
    u8 numShp;
    u8 firstUnusedMtxStackID;
    u8 dummy_;
    fx32 posScale;
    fx32 invPosScale;
    u16 numVertex;
    u16 numPolygon;
    u16 numTriangle;
    u16 numQuad;
    fx16 boxX, boxY, boxZ;
    fx16 boxW, boxH, boxD;
    fx32 boxPosScale;
    fx32 boxInvPosScale;
} NNSG3dResMdlInfo;
typedef enum {
    NNS_G3D_SRTFLAG_TRANS_ZERO        = 0x0001,
    NNS_G3D_SRTFLAG_ROT_ZERO          = 0x0002,
    NNS_G3D_SRTFLAG_SCALE_ONE         = 0x0004,
    NNS_G3D_SRTFLAG_PIVOT_EXIST       = 0x0008,
    NNS_G3D_SRTFLAG_IDXPIVOT_MASK     = 0x00f0,
    NNS_G3D_SRTFLAG_PIVOT_MINUS       = 0x0100,
    NNS_G3D_SRTFLAG_SIGN_REVC         = 0x0200,
    NNS_G3D_SRTFLAG_SIGN_REVD         = 0x0400,
    NNS_G3D_SRTFLAG_IDXMTXSTACK_MASK  = 0xf800,
    NNS_G3D_SRTFLAG_IDENTITY          = NNS_G3D_SRTFLAG_TRANS_ZERO |
                                        NNS_G3D_SRTFLAG_ROT_ZERO |
                                        NNS_G3D_SRTFLAG_SCALE_ONE,
    NNS_G3D_SRTFLAG_IDXPIVOT_SHIFT    = 4,
    NNS_G3D_SRTFLAG_IDXMTXSTACK_SHIFT = 11
} NNSG3dSRTFlag;
typedef struct NNSG3dResNodeInfo_ {
    NNSG3dResDict dict;
} NNSG3dResNodeInfo;
typedef struct NNSG3dResMdl_ {
    u32 size;
    u32 ofsSbc;
    u32 ofsMat;
    u32 ofsShp;
    u32 ofsEvpMtx;
    NNSG3dResMdlInfo info;
    NNSG3dResNodeInfo nodeInfo;
} NNSG3dResMdl;
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
struct NNSG3dMatAnmResult_;
struct NNSG3dJntAnmResult_;
struct NNSG3dVisAnmResult_;
typedef BOOL (*NNSG3dFuncAnmBlendMat)(struct NNSG3dMatAnmResult_ *, const NNSG3dAnmObj *, u32);
typedef BOOL (*NNSG3dFuncAnmBlendJnt)(struct NNSG3dJntAnmResult_ *, const NNSG3dAnmObj *, u32);
typedef BOOL (*NNSG3dFuncAnmBlendVis)(struct NNSG3dVisAnmResult_ *, const NNSG3dAnmObj *, u32);
struct NNSG3dRS_;
typedef void (*NNSG3dSbcCallBackFunc)(struct NNSG3dRS_ *);
typedef struct NNSG3dRenderObj_ {
    u32 flag;
    NNSG3dResMdl * resMdl;
    NNSG3dAnmObj * anmMat;
    NNSG3dFuncAnmBlendMat funcBlendMat;
    NNSG3dAnmObj * anmJnt;
    NNSG3dFuncAnmBlendJnt funcBlendJnt;
    NNSG3dAnmObj * anmVis;
    NNSG3dFuncAnmBlendVis funcBlendVis;
    NNSG3dSbcCallBackFunc cbFunc;
    u8 cbCmd;
    u8 cbTiming;
    u16 dummy_;
    NNSG3dSbcCallBackFunc cbInitFunc;
    void * ptrUser;
    u8 * ptrUserSbc;
    struct NNSG3dJntAnmResult_ * recJntAnm;
    struct NNSG3dMatAnmResult_ * recMatAnm;
    u32 hintMatAnmExist[64 / 32];
    u32 hintJntAnmExist[64 / 32];
    u32 hintVisAnmExist[64 / 32];
} NNSG3dRenderObj;
struct NNSG3dResMdl_;
typedef enum {
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE  = 0x00000001,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_ROTZERO   = 0x00000002,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO = 0x00000004,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SET       = 0x00000008,
    NNS_G3D_MATANM_RESULTFLAG_TEXMTX_MULT      = 0x00000010,
    NNS_G3D_MATANM_RESULTFLAG_WIREFRAME        = 0x00000020}
NNSG3dMatAnmResultFlag;
typedef struct NNSG3dMatAnmResult_ {
    NNSG3dMatAnmResultFlag flag;
    u32 prmMatColor0;
    u32 prmMatColor1;
    u32 prmPolygonAttr;
    u32 prmTexImage;
    u32 prmTexPltt;
    fx32 scaleS, scaleT;
    fx16 sinR, cosR;
    fx32 transS, transT;
    u16 origWidth, origHeight;
    fx32 magW, magH;
} NNSG3dMatAnmResult;
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
typedef struct NNSG3dVisAnmResult_ {
    BOOL isVisible;
} NNSG3dVisAnmResult;
void native_main_0202d0ac(NNSG3dJntAnmResult * pResult, const fx32 * p, const u8 * cmd, u32 srtflag);
typedef void (*NNSG3dGetJointScale)(NNSG3dJntAnmResult * pResult, const fx32 * p, const u8 * cmd, u32 srtflag);
typedef void (*NNSG3dSendJointSRT)(const NNSG3dJntAnmResult *);
typedef void (*NNSG3dSendTexSRT)(const NNSG3dMatAnmResult *);
typedef struct NNSG3dRS_ {
    u8 * c;
    NNSG3dRenderObj * pRenderObj;
    u32 flag;
    NNSG3dSbcCallBackFunc cbVecFunc[0x20 ];
    u8 cbVecTiming[0x20 ];
    u8 currentNode;
    u8 currentMat;
    u8 currentNodeDesc;
    u8 dummy_;
    NNSG3dMatAnmResult * pMatAnmResult;
    NNSG3dJntAnmResult * pJntAnmResult;
    NNSG3dVisAnmResult * pVisAnmResult;
    u32 isMatCached[64 / 32];
    u32 isScaleCacheOne[64 / 32];
    u32 isEvpCached[64 / 32];
    const NNSG3dResNodeInfo * pResNodeInfo;
    const NNSG3dResMat * pResMat;
    const NNSG3dResShp * pResShp;
    fx32 posScale;
    fx32 invPosScale;
    NNSG3dGetJointScale funcJntScale;
    NNSG3dSendJointSRT funcJntMtx;
    NNSG3dSendTexSRT funcTexMtx;
    NNSG3dMatAnmResult tmpMatAnmResult;
    NNSG3dJntAnmResult tmpJntAnmResult;
    NNSG3dVisAnmResult tmpVisAnmResult;
} NNSG3dRS;
typedef struct NNSG3dRSOnGlb_ {
    struct NNSG3dMatAnmResult_ matCache[64 ];
    struct {
        VecFx32 s;
        VecFx32 inv;
    } scaleCache[64 ];
    struct {
        MtxFx44 M;
        MtxFx33 N;
    } evpCache[64 ];
} NNSG3dRSOnGlb;
extern NNSG3dRS * native_data_main_020ee1f4;
extern NNSG3dRSOnGlb native_data_main_020ee1f8;
inline BOOL NNSi_G3dBitVecCheck(const u32 * vec, u32 idx);
inline void NNSi_G3dBitVecSet(u32 * vec, u32 idx);
inline void NNSi_G3dBitVecReset(u32 * vec, u32 idx);
static inline void MI_CpuCopy32 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c28(src, dest, size);
}
inline BOOL NNSi_G3dBitVecCheck (const u32 * vec, u32 idx)
{
    ((void) 0) ;
    return (BOOL)(vec[idx >> 5] & (1 << (idx & 31)));
}
inline void NNSi_G3dBitVecSet (u32 * vec, u32 idx)
{
    ((void) 0) ;
    vec[idx >> 5] |= 1 << (idx & 31);
}
inline void NNSi_G3dBitVecReset (u32 * vec, u32 idx)
{
    ((void) 0) ;
    vec[idx >> 5] &= ~(1 << (idx & 31));
}
