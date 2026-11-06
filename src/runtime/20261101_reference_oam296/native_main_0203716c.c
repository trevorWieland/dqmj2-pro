#pragma ipa file
#pragma enumsalwaysint on
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef int BOOL;
void native_fn_02008c14 (u32 data, void * destp, u32 size);
static inline void MI_CpuFill32 (void * dest, u32 data, u32 size)
{
    native_fn_02008c14 (data, dest, size);
}
typedef s32 fx32;
extern u32 native_data_020dcb44 ;
void native_fn_020072d0 (void * startAddr, u32 nBytes);
void native_fn_0200845c (u32 dmaNo, void * dest, u32 data, u32 size);
static u32 GX_GetDefaultDMA(void);
static inline u32 GX_GetDefaultDMA (void)
{
    return native_data_020dcb44 ;
}
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
inline void NNSi_G2dDmaFill32 (u32 dmaNo, void * dest, u32 data, u32 size)
{
    if (dmaNo != ((u32) ~0) ) {
        native_fn_0200845c (dmaNo, dest, data, size);
    } else {
        MI_CpuFill32(dest, data, size);
    }
}
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
static inline GXOamAttr * GetOamFromPtr_ (NNSG2dOamManagerInstance * pMan)
{
    {
        GXOamAttr * pFrom = GetOamBufferPtr_(pMan->type,
                                             pMan->managedAttrArea.fromIdx);
        return pFrom;
    }
}
static inline u32 GetSizeOfManageArea_ (const NNSG2dOAMManageArea * pArea)
{
    if (IsManageAreaValid_(pArea)) {
        return (u32)(sizeof(GXOamAttr) * (u16)(pArea->toIdx - pArea->fromIdx + 1));
    } else {
        return 0;
    }
}
static inline void ResetOam_ (NNSG2dOamType type, u16 fromIdx, u16 toIdx)
{
    GXOamAttr * pFrom = GetOamBufferPtr_(type, fromIdx);
    const u16 numArea = (u16)(toIdx - fromIdx + 1);
    u16 i;
    for (i = 0; i < numArea; i++) {
        *((u16 *)pFrom) = 192 ;
        pFrom++;
    }
}
unsigned int native_main_0203716c(signed int raw)
{
    NNSG2dOamManagerInstance * pMan = (NNSG2dOamManagerInstance *)raw;
    {
        if (pMan->bFastTransferEnable) {
            const u32 szByte = GetSizeOfManageArea_(&pMan->managedAttrArea);
            void * pData = GetOamFromPtr_(pMan);
            native_fn_020072d0 (pData, szByte);
            NNSi_G2dDmaFill32(GX_GetDefaultDMA() , pData, 192 , szByte);
        } else {
            ResetOam_(pMan->type,
                      pMan->managedAttrArea.fromIdx,
                      pMan->managedAttrArea.toIdx);
        }
    }
    {
        pMan->managedAttrArea.currentIdx = pMan->managedAttrArea.fromIdx;
    }
    return pMan->managedAffineArea.currentIdx = pMan->managedAffineArea.fromIdx;
}
