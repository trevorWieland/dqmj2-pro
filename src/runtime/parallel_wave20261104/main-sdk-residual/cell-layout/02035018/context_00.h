typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed long s32;
typedef int BOOL;
typedef s32 fx32;
extern const u16 (*ctrdgi_fl_maxtime);
typedef struct NNSG2dSVec2 {
    s16 x;
    s16 y;
} NNSG2dSVec2;
typedef struct NNSG2dFVec2 {
    fx32 x;
    fx32 y;
} NNSG2dFVec2;
typedef union {
        struct {
            fx32 _00, _01;
            fx32 _10, _11;
            fx32 _20, _21;
        };
        fx32 m[3][2];
        fx32 a[6];
    }
    MtxFx32;
typedef enum {
    NNS_G2D_SRTCONTROLTYPE_INVALID,
    NNS_G2D_SRTCONTROLTYPE_SRT,
    NNS_G2D_SRTCONTROLTYPE_MTX2D,
    NNS_G2D_SRTCONTROLTYPE_MTX3D,
    NNS_G2D_SRTCONTROLTYPE_MAX
} NNSG2dSRTControlType;
typedef union {
    struct {
        NNSG2dFVec2 scale;
        NNSG2dSVec2 trans;
        u16 rotZ;
        u16 SRT_EnableFlag;
    };
    MtxFx32 mtx;
} NNSG2dSRTData;
typedef struct {
    NNSG2dSRTControlType type;
    NNSG2dSRTData srtData;
} NNSG2dSRTControl;
typedef enum NNSG2dAnimationElement {
    NNS_G2D_ANIMELEMENT_INDEX = 0x0,
    NNS_G2D_ANIMELEMENT_INDEX_SRT,
    NNS_G2D_ANIMELEMENT_INDEX_T,
    NNS_G2D_ANIMELEMENT_MAX
} NNSG2dAnimationElement;
typedef enum NNSG2dAnimationPlayMode {
    NNS_G2D_ANIMATIONPLAYMODE_INVALID = 0x0,
    NNS_G2D_ANIMATIONPLAYMODE_FORWARD,
    NNS_G2D_ANIMATIONPLAYMODE_FORWARD_LOOP,
    NNS_G2D_ANIMATIONPLAYMODE_REVERSE,
    NNS_G2D_ANIMATIONPLAYMODE_REVERSE_LOOP,
    NNS_G2D_ANIMATIONPLAYMODE_MAX
} NNSG2dAnimationPlayMode;
typedef struct NNSG2dAnimDataSRT {
    u16 index;
    u16 rotZ;
    fx32 sx;
    fx32 sy;
    s16 px;
    s16 py;
} NNSG2dAnimDataSRT;
typedef struct NNSG2dAnimDataT {
    u16 index;
    u16 pad_;
    s16 px;
    s16 py;
} NNSG2dAnimDataT;
typedef struct NNSG2dAnimFrameData {
    void * pContent;
    u16 frames;
    u16 pad16;
} NNSG2dAnimFrameData;
typedef struct NNSG2dAnimSequenceData {
    u16 numFrames;
    u16 loopStartFrameIdx;
    u32 animType;
    NNSG2dAnimationPlayMode playMode;
    NNSG2dAnimFrameData * pAnmFrameArray;
} NNSG2dAnimSequenceData;
typedef enum NNSG2dCharacterDataMappingType {
    NNS_G2D_CHARACTERMAPPING_1D_32,
    NNS_G2D_CHARACTERMAPPING_1D_64,
    NNS_G2D_CHARACTERMAPPING_1D_128,
    NNS_G2D_CHARACTERMAPPING_1D_256,
    NNS_G2D_CHARACTERMAPPING_2D,
    NNS_G2D_CHARACTERMAPPING_MAX
} NNSG2dCharacterDataMappingType;
typedef struct NNSG2dCellVramTransferData {
    u32 srcDataOffset;
    u32 szByte;
} NNSG2dCellVramTransferData;
typedef struct NNSG2dVramTransferData {
    u32 szByteMax;
    NNSG2dCellVramTransferData * pCellTransferDataArray;
} NNSG2dVramTransferData;
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
typedef struct NNSG2dCellDataBank {
    u16 numCells;
    u16 cellBankAttr;
    NNSG2dCellData * pCellDataArrayHead;
    NNSG2dCharacterDataMappingType mappingMode;
    NNSG2dVramTransferData * pVramTransferData;
    void * pStringBank;
    void * pExtendedData;
} NNSG2dCellDataBank;
typedef NNSG2dAnimFrameData NNSG2dAnimFrame;
typedef NNSG2dAnimSequenceData NNSG2dAnimSequence;
typedef void (*NNSG2dAnmCallBackPtr)(u32 data, fx32 currentFrame);
typedef enum NNSG2dAnmCallbackType {
    NNS_G2D_ANMCALLBACKTYPE_NONE = 0,
    NNS_G2D_ANMCALLBACKTYPE_LAST_FRM,
    NNS_G2D_ANMCALLBACKTYPE_SPEC_FRM,
    NNS_G2D_ANMCALLBACKTYPE_EVER_FRM,
    AnmCallbackType_MAX
} NNSG2dAnmCallbackType;
typedef struct NNSG2dCallBackFunctor {
    NNSG2dAnmCallbackType type;
    u32 param;
    NNSG2dAnmCallBackPtr pFunc;
    u16 frameIdx;
    u16 pad16_;
} NNSG2dCallBackFunctor, NNSG2dAnimCallBackFunctor;
typedef struct NNSG2dAnimController {
    const NNSG2dAnimFrame * pCurrent;
    const NNSG2dAnimFrame * pActiveCurrent;
    BOOL bReverse;
    BOOL bActive;
    fx32 currentTime;
    fx32 speed;
    NNSG2dAnimationPlayMode overriddenPlayMode;
    const NNSG2dAnimSequence * pAnimSequence;
    NNSG2dAnimCallBackFunctor callbackFunctor;
} NNSG2dAnimController;
void * native_fn_02034d5c(NNSG2dAnimController * pAnimCtrl);
void native_fn_02035518(u32 handle, u32 srcOffset, u32 szByte);
typedef struct NNSG2dCellAnimation {
    NNSG2dAnimController animCtrl;
    const NNSG2dCellData * pCurrentCell;
    const NNSG2dCellDataBank * pCellDataBank;
    u32 cellTransferStateHandle;
    NNSG2dSRTControl srtCtrl;
} NNSG2dCellAnimation;
void native_fn_02037294(NNSG2dSRTControl * pCtrl, s16 x, s16 y);
void native_fn_020372b8(NNSG2dSRTControl * pCtrl, u16 rotZ);
void native_fn_020372d8(NNSG2dSRTControl * pCtrl, fx32 x, fx32 y);
void native_fn_020372f8(NNSG2dSRTControl * pCtrl, NNSG2dSRTControlType type);
const NNSG2dCellData * native_fn_020349f4(const NNSG2dCellDataBank * pCellData, u16 idx);
inline NNSG2dAnimationElement NNSi_G2dGetAnimSequenceElementType (u32 animType)
{
    return (NNSG2dAnimationElement)(animType & 0x00FF );
}
inline BOOL NNS_G2dCellDataBankHasVramTransferData (const NNSG2dCellDataBank * pCellBank)
{
    return (BOOL)(pCellBank->pVramTransferData != ((void *)0) );
}
inline const NNSG2dCellVramTransferData * NNSi_G2dGetCellVramTransferData (const NNSG2dCellDataBank * pCellBank, u16 cellIdx)
{
    const NNSG2dVramTransferData * pTransferData = pCellBank->pVramTransferData;
    return &pTransferData->pCellTransferDataArray[cellIdx];
}
inline BOOL NNSi_G2dIsCellAnimVramTransferHandleValid (const NNSG2dCellAnimation * pCellAnim)
{
    return (BOOL)(pCellAnim->cellTransferStateHandle != (u32)0xFFFFFFFF );
}
