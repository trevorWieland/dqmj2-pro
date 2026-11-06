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
typedef char NNSG2dChar;
typedef struct NNSG2dFont {
    NNSG2dFontInformation * pRes;
    NNSiG2dSplitCharCallback cbCharSpliter;
} NNSG2dFont;
typedef struct NNSG2dGlyph {
    const NNSG2dCharWidths * pWidths;
    const u8 * image;
} NNSG2dGlyph;
int native_fn_02036a8c(const NNSG2dFont * pFont, int vSpace, const void * txt);
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
typedef enum NNSG2dVerticalAlign {
    NNS_G2D_VERTICALALIGN_TOP    = 0x40,
    NNS_G2D_VERTICALALIGN_MIDDLE = 0x80,
    NNS_G2D_VERTICALALIGN_BOTTOM = 0x100
} NNSG2dVerticalAlign;
typedef struct NNSG2dTextCanvas {
    const NNSG2dCharCanvas * pCanvas;
    const NNSG2dFont * pFont;
    int hSpace;
    int vSpace;
} NNSG2dTextCanvas;
typedef struct NNSiG2dTextDirection {
    s8 x;
    s8 y;
} NNSiG2dTextDirection;
void native_fn_020373e4(const NNSG2dTextCanvas * pTxn, int x, int y, int areaWidth, int cl, u32 flags, const void * txt
                                     , NNSiG2dTextDirection d
                                     );
void native_main_02037670(const NNSG2dTextCanvas * pTxn, int x, int y, int w, int h, int cl, u32 flags, const void * txt
                                    , NNSiG2dTextDirection d
                                    );
void native_fn_020373e4 (const NNSG2dTextCanvas * pTxn, int x, int y, int areaWidth, int cl, u32 flags, const void * txt
                                      , NNSiG2dTextDirection d
                                      );
inline int NNS_G2dFontGetTextHeight (const NNSG2dFont * pFont, int vSpace, const NNSG2dChar * txt)
{
    return native_fn_02036a8c(pFont, vSpace, txt);
}
inline int NNS_G2dTextCanvasGetTextHeight (const NNSG2dTextCanvas * pTxn, const NNSG2dChar * txt)
{
    return NNS_G2dFontGetTextHeight(
        pTxn->pFont,
        pTxn->vSpace,
        txt);
}
