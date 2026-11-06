typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed char s8;
void native_fn_02008c58(u32 data, void * destp, u32 size);
static inline void MI_CpuFillFast (void * dest, u32 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c58(data, dest, size);
}
extern const u16 (*ctrdgi_fl_maxtime);
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
typedef u16 (*NNSiG2dSplitCharCallback)(const void ** ppChar);
typedef struct NNSG2dFont {
    NNSG2dFontInformation * pRes;
    NNSiG2dSplitCharCallback cbCharSpliter;
} NNSG2dFont;
typedef struct NNSG2dGlyph {
    const NNSG2dCharWidths * pWidths;
    const u8 * image;
} NNSG2dGlyph;
struct NNSG2dCharCanvas;
typedef void (*NNSiG2dDrawGlyphFunc)(const struct NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, const NNSG2dGlyph * pGlyph);
typedef void (*NNSiG2dClearFunc)(const struct NNSG2dCharCanvas * pCC, int cl);
typedef void (*NNSiG2dClearAreaFunc)(const struct NNSG2dCharCanvas * pCC, int cl, int x, int y, int w, int h);
typedef struct NNSiG2dCharCanvasVTable {
    NNSiG2dDrawGlyphFunc pDrawGlyph;
    NNSiG2dClearFunc pClear;
    NNSiG2dClearAreaFunc pClearArea;
} NNSiG2dCharCanvasVTable;
typedef struct NNSG2dCharCanvas {
    u8 * charBase;
    int areaWidth;
    int areaHeight;
    u8 dstBpp;
    u8 reserved[3];
    u32 param;
    const NNSiG2dCharCanvasVTable * vtable;
} NNSG2dCharCanvas;
void native_main_02035d70(const NNSG2dCharCanvas * pCC, int cl);
static inline int GetCharacterSize (const NNSG2dCharCanvas * pCC)
{
    ((void) 0) ;
    return 8 * 8 * pCC->dstBpp / 8;
}
static inline u32 SpreadColor32 (const NNSG2dCharCanvas * pCC, int cl)
{
    u32 val = (u32)cl;
    ((void) 0) ;
    if ( pCC->dstBpp == 4 ) {
        ((void) 0) ;
        val = (val << 4) | val;
        val |= val << 8;
        val |= val << 16;
    } else {
        ((void) 0) ;
        val = (val << 8) | val;
        val |= val << 16;
    }
    return val;
}
void native_main_02035d70 (const NNSG2dCharCanvas * pCC, int cl)
{
    u32 data;
    ((void) 0) ;
    data = SpreadColor32(pCC, cl);
    MI_CpuFillFast(
        pCC->charBase,
        data,
        (u32)pCC->areaWidth * pCC->areaHeight * GetCharacterSize(pCC)
        );
}

typedef char verified_u32_width[(sizeof(u32)==4)?1:-1];
