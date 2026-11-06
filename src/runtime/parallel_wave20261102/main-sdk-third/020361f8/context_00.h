typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed char s8;
extern const u16 (*ctrdgi_fl_maxtime);
typedef enum NNSG2dFontGlyphFlag {
    NNS_G2D_FONT_FLAG_TBRL     = (1 << 0),
    NNS_G2D_FONT_FLAG_ROT_0    = (0 << 1),
    NNS_G2D_FONT_FLAG_ROT_90   = (1 << 1),
    NNS_G2D_FONT_FLAG_ROT_180  = (2 << 1),
    NNS_G2D_FONT_FLAG_ROT_270  = (3 << 1),
    NNS_G2D_FONT_FLAG_ROT_MASK = (3 << 1)
} NNSG2dFontGlyphFlag;
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
u16 native_fn_0203694c(const NNSG2dFont * pFont, u16 c);
const NNSG2dCharWidths * native_fn_02036994(const NNSG2dFont * pFont, u16 idx);
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
int native_main_020361f8(const NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, u16 ccode);
inline u8 NNS_G2dFontGetCellHeight (const NNSG2dFont * pFont)
{
    ((void) 0) ;
    return pFont->pRes->pGlyph->cellHeight;
}
inline u8 NNS_G2dFontGetCellWidth (const NNSG2dFont * pFont)
{
    ((void) 0) ;
    return pFont->pRes->pGlyph->cellWidth;
}
inline int NNSi_G2dFontGetGlyphDataSize (const NNSG2dFont * pFont)
{
    ((void) 0) ;
    return pFont->pRes->pGlyph->cellSize;
}
inline const u8 * NNS_G2dFontGetGlyphImageFromIndex (const NNSG2dFont * pFont, u16 idx)
{
    ((void) 0) ;
    ((void) 0) ;
    return pFont->pRes->pGlyph->glyphTable + idx * NNSi_G2dFontGetGlyphDataSize(pFont);
}
inline u8 NNS_G2dFontGetFlags (const NNSG2dFont * pFont)
{
    ((void) 0) ;
    return pFont->pRes->pGlyph->flags;
}
inline u16 NNS_G2dFontGetGlyphIndex (const NNSG2dFont * pFont, u16 c)
{
    const u16 idx = native_fn_0203694c(pFont, c);
    return (idx != 0xFFFF ) ? idx : pFont->pRes->alterCharIndex;
}
inline void NNS_G2dFontGetGlyphFromIndex (NNSG2dGlyph * pGlyph, const NNSG2dFont * pFont, u16 idx)
{
    ((void) 0) ;
    ((void) 0); ;
    pGlyph->pWidths = native_fn_02036994(pFont, idx);
    pGlyph->image = NNS_G2dFontGetGlyphImageFromIndex(pFont, idx);
}
inline void NNS_G2dFontGetGlyph (NNSG2dGlyph * pGlyph, const NNSG2dFont * pFont, u16 ccode)
{
    u16 iGlyph;
    ((void) 0) ;
    ((void) 0); ;
    iGlyph = NNS_G2dFontGetGlyphIndex(pFont, ccode);
    NNS_G2dFontGetGlyphFromIndex(pGlyph, pFont, iGlyph);
}
inline void NNS_G2dCharCanvasDrawGlyph (const NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, const NNSG2dGlyph * pGlyph)
{
    ((void) 0) ;
    pCC->vtable->pDrawGlyph(pCC, pFont, x, y, cl, pGlyph);
}
