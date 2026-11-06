typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed long s32;
        typedef int BOOL;
typedef s32 fx32;
void native_fn_02007308(const void * startAddr, u32 nBytes);
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
void native_fn_020049fc(const void * pSrc, u32 offset, u32 szByte);
void native_fn_02004a50(const void * pSrc, u32 offset, u32 szByte);
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
void native_main_02036f68(signed int raw);
typedef void (OBJLoadFunction)(const void * pSrc, u32 offset, u32 szByte);
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
static inline OBJLoadFunction * GetOBJLoadFunction_ (NNSG2dOamType type)
{
    extern OBJLoadFunction * native_data_020dd810[5];
    return native_data_020dd810[type];
}
static inline void LoadOneAffine_ (const GXOamAffine * pAff, u32 offset, OBJLoadFunction * pOBJLoadFunc)
{
    offset += sizeof(u16) * 3 ;
    (*pOBJLoadFunc)(&pAff->PA, offset + sizeof(GXOamAttr) * 0, sizeof(u16));
    (*pOBJLoadFunc)(&pAff->PB, offset + sizeof(GXOamAttr) * 1, sizeof(u16));
    (*pOBJLoadFunc)(&pAff->PC, offset + sizeof(GXOamAttr) * 2, sizeof(u16));
    (*pOBJLoadFunc)(&pAff->PD, offset + sizeof(GXOamAttr) * 3, sizeof(u16));
}
static inline void LoadOamAndAffineFast_ (NNSG2dOamType type, u16 fromIdx, u16 toIdx)
{
    GXOamAttr * pFrom = GetOamBufferPtr_(type, fromIdx);
    const u16 szByte = (u16)(sizeof(GXOamAttr) * (toIdx - fromIdx + 1));
    u16 offset = (u16)(sizeof(GXOamAttr) * fromIdx);
    native_fn_02007308(pFrom, szByte);
    switch (type) {
    case NNS_G2D_OAMTYPE_MAIN:
        native_fn_020049fc(pFrom, offset, szByte);
        break;
    case NNS_G2D_OAMTYPE_SUB:
        native_fn_02004a50(pFrom, offset, szByte);
        break;
    default:
        break;
    }
}
static inline void LoadOam_ (NNSG2dOamType type, u16 fromIdx, u16 toIdx)
{
    GXOamAttr * pFrom = GetOamBufferPtr_(type, fromIdx);
    const u16 numArea = (u16)(toIdx - fromIdx + 1);
    u16 offset = (u16)(sizeof(GXOamAttr) * fromIdx);
    u16 i;
    OBJLoadFunction * pOBJLoadFunc = GetOBJLoadFunction_(type);
    for (i = 0; i < numArea; i++) {
        (*pOBJLoadFunc)(pFrom, offset, sizeof(u16) * 3 );
        offset += sizeof(GXOamAttr) ;
        pFrom++;
    }
}
static inline void LoadAffine_ (NNSG2dOamType type, u16 fromIdx, u16 toIdx)
{
    GXOamAffine * pFrom = GetAffineBufferPtr_(type, fromIdx);
    const u16 numArea = (u16)(toIdx - fromIdx + 1);
    u16 offset = (u16)(sizeof(GXOamAffine) * fromIdx);
    u16 i;
    OBJLoadFunction * pOBJLoadFunc = GetOBJLoadFunction_(type);
    for (i = 0; i < numArea; i++) {
        LoadOneAffine_(pFrom, offset, pOBJLoadFunc);
        offset += sizeof(GXOamAffine) ;
        pFrom++;
    }
}
void native_main_02036f68(signed int raw)
{
    NNSG2dOamManagerInstance *pMan = (NNSG2dOamManagerInstance *)raw;
    {
        if (pMan->bFastTransferEnable) {
            LoadOamAndAffineFast_(pMan->type,
                                  pMan->managedAttrArea.fromIdx,
                                  pMan->managedAttrArea.toIdx);
        } else {
            LoadOam_(pMan->type,
                     pMan->managedAttrArea.fromIdx,
                     pMan->managedAttrArea.toIdx);
            if (IsManageAreaValid_(&pMan->managedAffineArea)) {
                LoadAffine_(pMan->type,
                            pMan->managedAffineArea.fromIdx,
                            pMan->managedAffineArea.toIdx);
            }
        }
    }
}
