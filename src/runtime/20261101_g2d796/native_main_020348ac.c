typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned int u32;
typedef signed char s8;
typedef struct NNSG2dBinaryFileHeader {
    u32 signature;
    u16 byteOrder;
    u16 version;
    u32 fileSize;
    u16 headerSize;
    u16 dataBlocks;
} NNSG2dBinaryFileHeader;
typedef struct NNSG2dBinaryBlockHeader {
    u32 kind;
    u32 size;
} NNSG2dBinaryBlockHeader;
typedef struct NNSG2dCharWidths {
    s8 left;
    u8 glyphWidth;
    s8 charWidth;
} NNSG2dCharWidths;
typedef struct NNSG2dFontGlyph {
    u8 cellWidth;
    u8 cellHeight;
    u16 cellSize;
    s8 baselinePos;
    u8 maxCharWidth;
    u8 bpp;
    u8 flags;
    u8 glyphTable[];
} NNSG2dFontGlyph;
typedef struct NNSG2dFontWidth {
    u16 indexBegin;
    u16 indexEnd;
    struct NNSG2dFontWidth * pNext;
    NNSG2dCharWidths widthTable[];
} NNSG2dFontWidth;
typedef struct NNSG2dFontCodeMap {
    u16 ccodeBegin;
    u16 ccodeEnd;
    u16 mappingMethod;
    u16 reserved;
    struct NNSG2dFontCodeMap * pNext;
    u16 mapInfo[];
} NNSG2dFontCodeMap;
typedef struct NNSG2dFontInformation {
    u8 fontType;
    s8 linefeed;
    u16 alterCharIndex;
    NNSG2dCharWidths defaultWidth;
    u8 encoding;
    NNSG2dFontGlyph * pGlyph;
    NNSG2dFontWidth * pWidth;
    NNSG2dFontCodeMap * pMap;
} NNSG2dFontInformation;
void native_main_020348ac(void * rawObject);
static void inline ResolveOffset (void ** ppOffset, void * pBase)
{
    *ppOffset = (void *)(*(u32 *)ppOffset + (u32)pBase);
}
void native_main_020348ac (void * rawObject)
{
    NNSG2dBinaryFileHeader *pHeader = (NNSG2dBinaryFileHeader *)rawObject;
    NNSG2dBinaryBlockHeader * pBlock;
    NNSG2dFontInformation * pInfo = ((void *)0) ;
     ;
    {
        int nBlocks = 0;
        pBlock = (NNSG2dBinaryBlockHeader *)((u8 *)pHeader + pHeader->headerSize);
        while (nBlocks < pHeader->dataBlocks) {
            switch (pBlock->kind) {
            case (u32)'FINF' :
                {
                    pInfo = (NNSG2dFontInformation *)((u8 *)pBlock + sizeof(*pBlock));
                    ResolveOffset((void **)&(pInfo->pGlyph), pHeader);
                    if (pInfo->pWidth != ((void *)0) ) {
                        ResolveOffset((void **)&(pInfo->pWidth), pHeader);
                    }
                    if (pInfo->pMap != ((void *)0) ) {
                        ResolveOffset((void **)&(pInfo->pMap), pHeader);
                    }
                }
                break;
            case (u32)'CGLP' :
            {
                NNSG2dFontGlyph * pGlyph = (NNSG2dFontGlyph *)((u8 *)pBlock + sizeof(*pBlock));
            }
            break;
            case (u32)'CWDH' :
            {
                NNSG2dFontWidth * pWidth = (NNSG2dFontWidth *)((u8 *)pBlock + sizeof(*pBlock));
                if (pWidth->pNext != ((void *)0) ) {
                    ResolveOffset((void **)&(pWidth->pNext), pHeader);
                }
            }
            break;
            case (u32)'CMAP' :
            {
                NNSG2dFontCodeMap * pMap = (NNSG2dFontCodeMap *)((u8 *)pBlock + sizeof(*pBlock));
                if (pMap->pNext != ((void *)0) ) {
                    ResolveOffset((void **)&(pMap->pNext), pHeader);
                }
            }
            break;
            default:
                break;
            }
            pBlock = (NNSG2dBinaryBlockHeader *)((u8 *)pBlock + pBlock->size);
            nBlocks++;
        }
    }
}
