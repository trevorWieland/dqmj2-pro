typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
        typedef int BOOL;
void native_fn_02008be0(u16 data, void * destp, u32 size);
static inline void MI_CpuFill16 (void * dest, u16 data, u32 size)
{
	native_fn_02008be0(data, dest, size);
}
typedef s32 fx32;
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
BOOL native_main_02036c78(NNSG2dOamManagerInstance * pMan, u16 fromOBJ, u16 numOBJ, NNSG2dOamType type);
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
extern u16 native_data_020f0f04;
static inline OamCache * GetOamCachePtr_ (NNSG2dOamType type)
{
    return &native_data_020f0f08 [type];
}
static inline u16 * GetOamReservationTblPtr_ (NNSG2dOamType type)
{
    {
        OamCache * pOamCache = GetOamCachePtr_(type);
        return pOamCache->attributeCache.reservationTable;
    }
}
static inline u16 * GetAffineReservationTblPtr_ (NNSG2dOamType type)
{
    {
        OamCache * pOamCache = GetOamCachePtr_(type);
        return pOamCache->affineCache.reservationTable;
    }
}
static inline BOOL IsOamNotUsed_ (u16 * pResvTblHead, u16 from, u16 to)
{
    const u16 * pCursor = pResvTblHead + from;
    const u16 * pEnd = pResvTblHead + to;
    while (pCursor <= pEnd) {
        if (*pCursor != 0xFFFF ) {
            return 0 ;
        }
        pCursor++;
    }
    return 1 ;
}
static inline u16 GetNewGUID_ (void)
{
    return native_data_020f0f04++;
}
static inline void DoReserveArea_ (u16 * pResvTblHead, u16 from, u16 to, u16 ownerGUID)
{
    MI_CpuFill16(pResvTblHead + from, ownerGUID, sizeof(u16) * (u32)(to - from + 1));
}
BOOL native_main_02036c78 (NNSG2dOamManagerInstance * pMan, u16 fromOBJ, u16 numOBJ, NNSG2dOamType type)
{
    {
        u16 * pReserveTbl = GetOamReservationTblPtr_(type);
        const u16 toOBJ = (u16)(fromOBJ + (numOBJ - 1));
        if (IsOamNotUsed_(pReserveTbl, fromOBJ, toOBJ)) {
            pMan->GUID = GetNewGUID_();
            pMan->managedAttrArea.fromIdx = fromOBJ;
            pMan->managedAttrArea.toIdx = toOBJ;
            pMan->managedAttrArea.currentIdx = fromOBJ;
            DoReserveArea_(pReserveTbl, fromOBJ, toOBJ, pMan->GUID);
        } else {
            return 0 ;
        }
    }
    {
        const u16 fromAffine = (u16)(fromOBJ / 4);
        const u16 numAffine = (u16)(numOBJ / 4);
        const u16 toAffine = (u16)(fromAffine + (numAffine - 1));
        u16 * pReserveTbl = GetAffineReservationTblPtr_(type);
        if (IsOamNotUsed_(pReserveTbl, fromAffine, toAffine)) {
            pMan->managedAffineArea.fromIdx = fromAffine;
            pMan->managedAffineArea.toIdx = toAffine;
            pMan->managedAffineArea.currentIdx = fromAffine;
            DoReserveArea_(pReserveTbl, fromAffine, toAffine, pMan->GUID);
        } else {
            return 0 ;
        }
    }
    pMan->bFastTransferEnable = 1 ;
    pMan->type = type;
    return 1 ;
}
