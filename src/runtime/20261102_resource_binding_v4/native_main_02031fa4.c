typedef signed int s32;
typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
        typedef int BOOL;
extern const u16 (*ctrdgi_fl_maxtime);
typedef u32 NNSGfdTexKey;
typedef NNSGfdTexKey (*NNSGfdFuncAllocTexVram)(u32 szByte, BOOL is4x4comp, u32 opt);
typedef int (*NNSGfdFuncFreeTexVram)(NNSGfdTexKey key);
extern NNSGfdFuncAllocTexVram native_data_020dd8c0;
extern NNSGfdFuncFreeTexVram native_data_020dd8c4;
inline NNSGfdTexKey NNS_GfdAllocTexVram (u32 szByte, BOOL is4x4comp, u32 opt)
{
    return (*native_data_020dd8c0)(szByte, is4x4comp, opt);
}
inline int NNS_GfdFreeTexVram (NNSGfdTexKey memKey)
{
    return (*native_data_020dd8c4)(memKey);
}
typedef u32 NNSGfdPlttKey;
typedef NNSGfdPlttKey (*NNSGfdFuncAllocPlttVram)(u32 szByte, BOOL is4pltt, u32 opt);
typedef int (*NNSGfdFuncFreePlttVram)(NNSGfdPlttKey plttKey);
extern NNSGfdFuncAllocPlttVram native_data_020dd8b8;
extern NNSGfdFuncFreePlttVram native_data_020dd8bc;
inline NNSGfdPlttKey NNS_GfdAllocPlttVram (u32 szByte, BOOL is4pltt, u32 opt)
{
    return (*native_data_020dd8b8)(szByte, is4pltt, opt);
}
inline int NNS_GfdFreePlttVram (NNSGfdPlttKey plttKey)
{
    return (*native_data_020dd8bc)(plttKey);
}
typedef struct NNSG3dResFileHeader_ {
    union {
        char signature[4];
        u32 sigVal;
    };
    u16 byteOrder;
    u16 version;
    u32 fileSize;
    u16 headerSize;
    u16 dataBlocks;
} NNSG3dResFileHeader;
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
typedef enum {
    NNS_G3D_RESPLTT_LOADED   = 0x0001,
    NNS_G3D_RESPLTT_USEPLTT4 = 0x8000
} NNSG3dResPlttFlag;
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
typedef struct NNSG3dResMdlSet_ {
    NNSG3dResDataBlockHeader header;
    NNSG3dResDict dict;
} NNSG3dResMdlSet;
typedef u32 NNSG3dTexKey;
typedef u32 NNSG3dPlttKey;
extern u32 native_fn_0202ec30(void *);
extern u32 native_fn_0202ec44(void *);
extern void native_fn_0202ec58(void *, s32, s32);
extern void native_fn_0202ec6c(void *, s32);
extern u32 native_fn_0202ed70(void *);
extern u32 native_fn_0202ed84(void *, s32);
extern void native_fn_0202ed8c(void *, s32);
BOOL native_fn_0202f3dc(NNSG3dResMdlSet * pMdlSet, const NNSG3dResTex * pTex);
BOOL native_main_02031fa4(void * pResData);
NNSG3dResMdlSet * native_fn_0202bedc(const NNSG3dResFileHeader * header);
extern u32 native_fn_0202beec(void *);
BOOL native_main_02031fa4 (void * pResData)
{
    u8 * binFile = (u8 *)pResData;
    BOOL failed = 0 ;
    ((void) 0) ;
    switch (*(u32 *)&binFile[0]) {
    case '0XTB' :
    case '0DMB' :
    {
        NNSG3dResTex * tex;
        u32 szTex, szTex4x4, szPltt;
        BOOL sucTex = 1 ;
        BOOL sucTex4x4 = 1 ;
        BOOL sucPltt = 1 ;
        NNSG3dTexKey keyTex;
        NNSG3dTexKey keyTex4x4;
        NNSG3dPlttKey keyPltt;
        tex = (NNSG3dResTex *)native_fn_0202beec((void *)pResData);
        if (tex) {
            szTex = native_fn_0202ec30((void *)tex);
            szTex4x4 = native_fn_0202ec44((void *)tex);
            szPltt = native_fn_0202ed70((void *)tex);
            if (szTex > 0) {
                keyTex = NNS_GfdAllocTexVram(szTex, 0 , 0);
                if (keyTex == (u32)0x0 ) {
                    sucTex = 0 ;
                }
            } else {
                keyTex = 0;
            }
            if (szTex4x4 > 0) {
                keyTex4x4 = NNS_GfdAllocTexVram(szTex4x4, 1 , 0);
                if (keyTex4x4 == (u32)0x0 ) {
                    sucTex4x4 = 0 ;
                }
            } else {
                keyTex4x4 = 0;
            }
            if (szPltt > 0) {
                keyPltt =
                    NNS_GfdAllocPlttVram(szPltt,
                                         tex->tex4x4Info.flag & NNS_G3D_RESPLTT_USEPLTT4,
                                         0);
                if (keyPltt == (u32)0x0 ) {
                    sucPltt = 0 ;
                }
            } else {
                keyPltt = 0;
            }
            if (!sucTex || !sucTex4x4 || !sucPltt) {
                int status;
                if (sucPltt) {
                    status = NNS_GfdFreePlttVram(keyPltt);
                    ((void) 0) ;
                }
                if (sucTex4x4) {
                    status = NNS_GfdFreeTexVram(keyTex4x4);
                    ((void) 0) ;
                }
                if (sucTex) {
                    status = NNS_GfdFreeTexVram(keyTex);
                    ((void) 0) ;
                }
                return 0 ;
            }
            native_fn_0202ec58((void *)tex, (s32)keyTex, (s32)keyTex4x4);
            (void)native_fn_0202ed84((void *)tex, (s32)keyPltt);
            native_fn_0202ec6c((void *)tex, 1);
            native_fn_0202ed8c((void *)tex, 1);
        }
        if (*(u32 *)&binFile[0] == '0DMB' ) {
            NNSG3dResMdlSet * mdlSet = native_fn_0202bedc((NNSG3dResFileHeader *) pResData);
            ((void) 0) ;
            if (tex) {
                (void)native_fn_0202f3dc(mdlSet, tex);
            }
        }
    }
        return 1 ;
        break;
    case '0ACB' :
    case '0AVB' :
    case '0AMB' :
    case '0PTB' :
    case '0ATB' :
        return 1 ;
        break;
    default:
        ((void) 0)
                          ;
        return 0 ;
        break;
    };
}
