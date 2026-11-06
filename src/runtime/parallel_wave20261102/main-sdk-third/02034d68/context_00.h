typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef signed long long int s64;
typedef int BOOL;
typedef s32 fx32;
static fx32 FX_MulInline(fx32 v1, fx32 v2);
extern const u16 (*ctrdgi_fl_maxtime);
typedef enum NNSG2dAnimationPlayMode {
    NNS_G2D_ANIMATIONPLAYMODE_INVALID = 0x0,
    NNS_G2D_ANIMATIONPLAYMODE_FORWARD,
    NNS_G2D_ANIMATIONPLAYMODE_FORWARD_LOOP,
    NNS_G2D_ANIMATIONPLAYMODE_REVERSE,
    NNS_G2D_ANIMATIONPLAYMODE_REVERSE_LOOP,
    NNS_G2D_ANIMATIONPLAYMODE_MAX
} NNSG2dAnimationPlayMode;
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
BOOL native_main_02034d68(NNSG2dAnimController * pAnimCtrl, fx32 frames);
int native_fn_0201af84(int value);
void native_fn_02034c10 (NNSG2dAnimController * pAnimCtrl);
static inline fx32 FX32_CAST (s64 res)
    {
        ((void) 0) ;
        return (fx32)res;
    }
static inline fx32 FX_MulInline (fx32 v1, fx32 v2)
    {
        return FX32_CAST(((s64)(v1) * v2 + 0x800LL) >> 12 );
    }
static inline const NNSG2dAnimFrame * GetFrameEnd_ (const NNSG2dAnimSequence * pSequence)
{
    ((void) 0) ;
    return pSequence->pAnmFrameArray + (pSequence->numFrames);
}
static inline const NNSG2dAnimFrame * GetFrameLoopBegin_ (const NNSG2dAnimSequence * pSequence)
{
    ((void) 0) ;
    return pSequence->pAnmFrameArray + pSequence->loopStartFrameIdx;
}
static inline u16 GetCurrentFrameIdx_ (const NNSG2dAnimController * pAnimCtrl)
{
    ((void) 0) ;
    return (u16)(((u32)pAnimCtrl->pCurrent - (u32)pAnimCtrl->pAnimSequence->pAnmFrameArray)
                 / sizeof(NNSG2dAnimFrameData));
}
static inline BOOL IsAnimCtrlMovingForward_ (const NNSG2dAnimController * pAnimCtrl)
{
    ((void) 0) ;
    return (pAnimCtrl->speed > 0) ^ (pAnimCtrl->bReverse) ? 1 : 0 ;
}
static inline BOOL ShouldAnmCtrlMoveNext_ (NNSG2dAnimController * pAnimCtrl)
{
    ((void) 0) ;
    ((void) 0) ;
    if ( pAnimCtrl->bActive &&
         (pAnimCtrl->currentTime >= ((fx32) 0x0000000000001000L) * (int)pAnimCtrl->pCurrent->frames)) {
        return 1 ;
    }
    return 0 ;
}
static inline void CallbackFuncHandling_ (const NNSG2dCallBackFunctor * pFunctor, u16 currentFrameIdx)
{
    ((void) 0) ;
    switch ( pFunctor->type )
    {
    case NNS_G2D_ANMCALLBACKTYPE_SPEC_FRM:
        if ( currentFrameIdx == pFunctor->frameIdx ) {
            (*pFunctor->pFunc)(pFunctor->param, currentFrameIdx);
        }
        break;
    case NNS_G2D_ANMCALLBACKTYPE_EVER_FRM:
        (*pFunctor->pFunc)(pFunctor->param, currentFrameIdx);
        break;
    }
}
static inline BOOL IsReachStartEdge_ (const NNSG2dAnimController * pAnimCtrl, const NNSG2dAnimFrame * pFrame)
{
    ((void) 0) ;
    ((void) 0) ;
    return (pFrame <= (GetFrameLoopBegin_(pAnimCtrl->pAnimSequence) - 1)) ? 1 : 0 ;
}
static inline BOOL IsReachEdge_ (const NNSG2dAnimController * pAnimCtrl, const NNSG2dAnimFrame * pFrame)
{
    ((void) 0) ;
    ((void) 0) ;
    if ( IsAnimCtrlMovingForward_(pAnimCtrl)) {
        return (pFrame >= GetFrameEnd_(pAnimCtrl->pAnimSequence)) ? 1 : 0 ;
    } else {
        return IsReachStartEdge_(pAnimCtrl, pFrame);
    }
}
static inline void MoveNext_ (NNSG2dAnimController * pAnimCtrl)
{
    ((void) 0) ;
    if ( IsAnimCtrlMovingForward_(pAnimCtrl)) {
        pAnimCtrl->pCurrent++;
    } else {
        pAnimCtrl->pCurrent--;
    }
}
