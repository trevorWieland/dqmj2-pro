typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed char s8;
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
typedef union OBJ1DParam {
    u32 packed;
    struct {
        unsigned baseWidthShift :8;
        unsigned baseHeightShift :8;
    };
} OBJ1DParam;
void native_main_02035fdc(const NNSG2dCharCanvas * pCC, int cl, int x, int y, int w, int h);
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
u32 native_fn_0203553c (u32 cx, u32 cy, u32 areaWidth, u32 areaHeight, u32 objWidth, u32 objHeight);
void native_fn_02035650 (void * pChar, int x, int y, int w, int h, u32 cl8, int bpp);
void native_main_02035fdc (const NNSG2dCharCanvas * pCC, int cl, int x, int y, int w, int h)
{
    int ix, iy;
    int pcx, pcy, pcw, pch;
    int cx, cy;
    const int xw = x + w;
    const int yh = y + h;
    u32 cl8;
    OBJ1DParam p;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    cl8 = SpreadColor32(pCC, cl);
    p.packed = pCC->param;
    {
        const int left = ((x) & ~(( 8) - 1)) ;
        const int top = ((y) & ~(( 8) - 1)) ;
        const int right = (((xw) + (( 8) - 1)) & ~(( 8) - 1)) ;
        const int bottom = (((yh) + (( 8) - 1)) & ~(( 8) - 1)) ;
        const int areaWidth = pCC->areaWidth;
        const int areaHeight = pCC->areaHeight;
        const int baseWidthShift = (int)p.baseWidthShift;
        const int baseHeightShift = (int)p.baseHeightShift;
        const int charSize = GetCharacterSize(pCC);
        const int charBaseLineOffset = (int)pCC->param * charSize;
        const int bpp = pCC->dstBpp;
        const int cx_base = left / 8 ;
        u8 * const pCharBase = pCC->charBase;
        u8 * pChar;
        cy = top / 8 ;
        for (iy = top; iy < bottom; iy += 8 ) {
            pcy = (iy < y) ? y - iy: 0;
            pch = ((yh - iy > 8 ) ? 8 : yh - iy) - pcy;
            pChar = pCharBase;
            cx = cx_base;
            for (ix = left; ix < right; ix += 8 ) {
                const u32 iChar = native_fn_0203553c((u32)cx, (u32)cy, (u32)areaWidth, (u32)areaHeight, (u32)baseWidthShift, (u32)baseHeightShift);
                pcx = (ix < x) ? x - ix: 0;
                pcw = ((xw - ix > 8 ) ? 8 : xw - ix) - pcx;
                pChar = pCharBase + iChar * charSize;
                native_fn_02035650(pChar, pcx, pcy, pcw, pch, cl8, bpp);
                cx++;
            }
            cy++;
        }
    }
}

typedef char verified_u32_width[(sizeof(u32)==4)?1:-1];
