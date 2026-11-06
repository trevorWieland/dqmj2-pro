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
typedef enum NNSG2dCharaColorMode {
    NNS_G2D_CHARA_COLORMODE_16  = 4,
    NNS_G2D_CHARA_COLORMODE_256 = 8
} NNSG2dCharaColorMode;
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
void native_main_0203631c(NNSG2dCharCanvas * pCC, void * charBase, int areaWidth, int areaHeight, NNSG2dCharaColorMode colorMode);
static void DrawGlyphLine(const NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, const NNSG2dGlyph * pGlyph);
static void ClearContinuous(const NNSG2dCharCanvas * pCC, int cl);
static void ClearAreaLine(const NNSG2dCharCanvas * pCC, int cl, int x, int y, int w, int h);
extern const NNSiG2dCharCanvasVTable native_data_main_020d90e8;
void DrawGlyphLine (const NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, const NNSG2dGlyph * pGlyph);
void ClearContinuous (const NNSG2dCharCanvas * pCC, int cl);
void ClearAreaLine (const NNSG2dCharCanvas * pCC, int cl, int x, int y, int w, int h);
void native_fn_020361d0 (NNSG2dCharCanvas * pCC, void * charBase, int areaWidth, int areaHeight, NNSG2dCharaColorMode colorMode, const NNSiG2dCharCanvasVTable * vtable, u32 param);
void native_main_0203631c (NNSG2dCharCanvas * pCC, void * charBase, int areaWidth, int areaHeight, NNSG2dCharaColorMode colorMode)
{
    ((void) 0); ;
    ((void) 0); ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    native_fn_020361d0(
        pCC,
        charBase, areaWidth, areaHeight, colorMode,
        &native_data_main_020d90e8, (unsigned int)areaWidth
        );
}
