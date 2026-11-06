typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed long s32;
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
typedef struct {
    u16 _0;
    u16 _1;
    u16 _2;
    s16 PA;
    u16 _4;
    u16 _5;
    u16 _6;
    s16 PB;
    u16 _8;
    u16 _9;
    u16 _10;
    s16 PC;
    u16 _12;
    u16 _13;
    u16 _14;
    s16 PD;
} GXOamAffine;
static void G2_SetOBJAffine(GXOamAffine * oam, const MtxFx22 * mtx);
static inline void G2_SetOBJAffine (GXOamAffine * oam, const MtxFx22 * mtx)
{
    oam->PA = (s16)(mtx->_00 >> 4);
    oam->PB = (s16)(mtx->_01 >> 4);
    oam->PC = (s16)(mtx->_10 >> 4);
    oam->PD = (s16)(mtx->_11 >> 4);
}
typedef enum NNSG2dOamType {
    NNS_G2D_OAMTYPE_MAIN = 0,
    NNS_G2D_OAMTYPE_SUB,
    NNS_G2D_OAMTYPE_SOFTWAREEMULATION,
    NNS_G2D_OAMTYPE_INVALID,
    NNS_G2D_OAMTYPE_MAX
} NNSG2dOamType;
typedef struct NNSG2dOAMManageArea {
    u16 fromIdx;
    u16 toIdx;
    u16 currentIdx;
} NNSG2dOAMManageArea;
typedef struct NNSG2dOamManagerInstance {
    NNSG2dOamType type;
    NNSG2dOAMManageArea managedAttrArea;
    NNSG2dOAMManageArea managedAffineArea;
    u16 GUID;
    u16 pad16_;
    BOOL bFastTransferEnable;
    fx32 spriteZoffsetStep;
} NNSG2dOamManagerInstance;
u16 native_main_02036ea4(NNSG2dOamManagerInstance * pMan, const MtxFx22 * mtx);
typedef struct OamAttributeCache {
    u16 reservationTable[128 ];
    GXOamAttr oamBuffer[128 ];
} OamAttributeCache;
typedef struct OamAffineCache {
    u16 reservationTable[32 ];
} OamAffineCache;
typedef struct OamCache {
    OamAttributeCache attributeCache;
    OamAffineCache affineCache;
} OamCache;
extern OamCache native_data_020f0f08 [3 ];
static inline BOOL IsManageAreaValid_ (const NNSG2dOAMManageArea * pArea)
{
    return (BOOL)((pArea->currentIdx <= pArea->toIdx + 1) &&
                  (pArea->fromIdx <= pArea->toIdx));
}
static inline OamCache * GetOamCachePtr_ (NNSG2dOamType type)
{
    return &native_data_020f0f08 [type];
}
static inline GXOamAttr * GetOamBufferPtr_ (NNSG2dOamType type, u16 index)
{
    {
        OamCache * pOamCache = GetOamCachePtr_(type);
        return pOamCache->attributeCache.oamBuffer + index;
    }
}
static inline GXOamAffine * GetAffineBufferPtr_ (NNSG2dOamType type, u16 index)
{
    {
        GXOamAffine * pAff = (GXOamAffine *)GetOamBufferPtr_(type, 0);
        return pAff + index;
    }
}
static inline u16 GetCapacity_ (const NNSG2dOAMManageArea * pArea)
{
    if (IsManageAreaValid_(pArea)) {
        return (u16)((int)pArea->toIdx - pArea->currentIdx + 1);
    } else {
        return 0;
    }
}
static inline BOOL HasEnoughCapacity_ (const NNSG2dOAMManageArea * pArea, u16 num)
{
    return (BOOL)(GetCapacity_(pArea) >= num);
}
static inline void SetAffineParams_ (NNSG2dOamType type, const MtxFx22 * mtx, u16 idx)
{
    {
        GXOamAffine * pAff = GetAffineBufferPtr_(type, idx);
        G2_SetOBJAffine(pAff, mtx);
    }
}
u16 native_main_02036ea4 (NNSG2dOamManagerInstance * pMan, const MtxFx22 * mtx)
{
    if (HasEnoughCapacity_(&pMan->managedAffineArea, 1)) {
        const u16 currentAffineIdx = pMan->managedAffineArea.currentIdx;
        SetAffineParams_(pMan->type, mtx, currentAffineIdx);
        pMan->managedAffineArea.currentIdx++;
        return currentAffineIdx;
    } else {
        return 0xFFFE ;
    }
}
