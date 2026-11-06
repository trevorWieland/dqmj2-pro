typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed short int s16;
typedef signed long s32;
typedef s32 fx32;
typedef s16 fx16;
extern const u16 (*ctrdgi_fl_maxtime);
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
typedef struct NNSG3dResDictEntryHeader_ {
    u16 sizeUnit;
    u16 ofsName;
    u8 data[4];
} NNSG3dResDictEntryHeader;
typedef struct NNSG3dResAnmHeader_ {
    u8 category0;
    u8 revision;
    u16 category1;
} NNSG3dResAnmHeader;
typedef struct NNSG3dResDictTexSRTAnmData_ {
    u32 scaleS;
    u32 scaleSEx;
    u32 scaleT;
    u32 scaleTEx;
    u32 rot;
    u32 rotEx;
    u32 transS;
    u32 transSEx;
    u32 transT;
    u32 transTEx;
} NNSG3dResDictTexSRTAnmData;
typedef struct NNSG3dResTexSRTAnm_ {
    NNSG3dResAnmHeader anmHeader;
    u16 numFrame;
    u8 flag;
    u8 texMtxMode;
    NNSG3dResDict dict;
} NNSG3dResTexSRTAnm;
struct NNSG3dMatAnmResult_;
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
inline void * NNS_G3dGetResDataByIdx(const NNSG3dResDict * dict, u32 idx);
inline void * NNS_G3dGetResDataByIdx (const NNSG3dResDict * dict, u32 idx)
{
    NNSG3dResDictEntryHeader * hdr;
    ((void) 0) ;
    if (dict != ((void *)0) && idx < dict->numEntry) {
        ((void) 0) ;
        hdr = (NNSG3dResDictEntryHeader *)((u8 *)dict + dict->ofsEntry);
        return (void *)(&hdr->data[0] + hdr->sizeUnit * idx);
    } else {
        return ((void *)0) ;
    }
}
fx32 native_fn_02033d48 (const NNSG3dResTexSRTAnm * pTexAnm, u32 info, u32 data, u32 frame);
u32 native_fn_02033e48 (const NNSG3dResTexSRTAnm * pTexAnm, u32 info, u32 data, u32 frame);
void native_main_02033f54 (const NNSG3dResTexSRTAnm * pTexAnm, u16 idx, u32 frame, NNSG3dMatAnmResult * pResult)
{
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    {
        const NNSG3dResDictTexSRTAnmData * pAnmData =
            (const NNSG3dResDictTexSRTAnmData *)NNS_G3dGetResDataByIdx(&pTexAnm->dict, idx);
        NNSG3dMatAnmResultFlag flag = pResult->flag;
        {
            fx32 transS, transT;
            transS = native_fn_02033d48(pTexAnm,
                                            pAnmData->transS,
                                            pAnmData->transSEx,
                                            frame);
            transT = native_fn_02033d48(pTexAnm,
                                            pAnmData->transT,
                                            pAnmData->transTEx,
                                            frame);
            if (transS == 0 && transT == 0) {
                flag |= NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO;
            } else {
                flag &= ~NNS_G3D_MATANM_RESULTFLAG_TEXMTX_TRANSZERO;
                pResult->transS = transS;
                pResult->transT = transT;
            }
        }
        {
            u32 data = native_fn_02033e48(pTexAnm,
                                              pAnmData->rot,
                                              pAnmData->rotEx,
                                              frame);
            if (data == ((((fx32) 0x0000000000001000L) << 16) | 0)) {
                flag |= NNS_G3D_MATANM_RESULTFLAG_TEXMTX_ROTZERO;
            } else {
                pResult->sinR = (fx16)(data & 0x0000FFFF);
                pResult->cosR = (fx16)(data >> 16);
                flag &= ~NNS_G3D_MATANM_RESULTFLAG_TEXMTX_ROTZERO;
            }
        }
        {
            fx32 scaleS, scaleT;
            scaleS = native_fn_02033d48(pTexAnm,
                                            pAnmData->scaleS,
                                            pAnmData->scaleSEx,
                                            frame);
            scaleT = native_fn_02033d48(pTexAnm,
                                            pAnmData->scaleT,
                                            pAnmData->scaleTEx,
                                            frame);
            if (scaleS == ((fx32) 0x0000000000001000L) && scaleT == ((fx32) 0x0000000000001000L) ) {
                flag |= NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE;
            } else {
                flag &= ~NNS_G3D_MATANM_RESULTFLAG_TEXMTX_SCALEONE;
                pResult->scaleS = scaleS;
                pResult->scaleT = scaleT;
            }
        }
        pResult->flag = flag;
    }
}

typedef char checked_u32_width[(sizeof(u32)==4)?1:-1];
