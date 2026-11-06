typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed char s8;
typedef struct {
        union {
            u32 attr01;
            struct {
                u16 attr0;
                u16 attr1;
            };
            struct {
                u32 y : 8;
                u32 rsMode : 2;
                u32 objMode : 2;
                u32 mosaic : 1;
                u32 colorMode : 1;
                u32 shape : 2;
                u32 x : 9;
                u32 rsParam : 5;
                u32 size : 2;
            };
            struct {
                u32 _0 : 28;
                u32 flipH : 1;
                u32 flipV : 1;
                u32 _1 : 2;
            };
        };
        union {
            struct {
                u16 attr2;
                u16 _3;
            };
            u32 attr23;
            struct {
                u32 charNo : 10;
                u32 priority : 2;
                u32 cParam : 4;
                u32 _2 : 16;
            };
        };
    } GXOamAttr;
typedef enum {
    GX_OAM_SHAPE_8x8   = (0 << 14 ) | (0 << 30 ),
    GX_OAM_SHAPE_16x16 = (0 << 14 ) | (1 << 30 ),
    GX_OAM_SHAPE_32x32 = (0 << 14 ) | (2 << 30 ),
    GX_OAM_SHAPE_64x64 = (0 << 14 ) | (3 << 30 ),
    GX_OAM_SHAPE_16x8  = (1 << 14 ) | (0 << 30 ),
    GX_OAM_SHAPE_32x8  = (1 << 14 ) | (1 << 30 ),
    GX_OAM_SHAPE_32x16 = (1 << 14 ) | (2 << 30 ),
    GX_OAM_SHAPE_64x32 = (1 << 14 ) | (3 << 30 ),
    GX_OAM_SHAPE_8x16  = (2 << 14 ) | (0 << 30 ),
    GX_OAM_SHAPE_8x32  = (2 << 14 ) | (1 << 30 ),
    GX_OAM_SHAPE_16x32 = (2 << 14 ) | (2 << 30 ),
    GX_OAM_SHAPE_32x64 = (2 << 14 ) | (3 << 30 )
} GXOamShape;
typedef enum {
    GX_OAM_COLORMODE_16  = 0,
    GX_OAM_COLORMODE_256 = 1
} GXOamColorMode;
static void G2_SetOBJPosition(GXOamAttr * oam, int x, int y);
static void G2_SetOBJShape(GXOamAttr * oam, GXOamShape shape);
static void G2_SetOBJCharName(GXOamAttr * oam, int name);
static void G2_SetOBJColorMode(GXOamAttr * oam, GXOamColorMode color);
static inline void G2_SetOBJPosition (GXOamAttr * oam, int x, int y)
{
    oam->attr01 = ((oam->attr01 & ~(0x000000ff | 0x01ff0000 )) |
                   (y & 0x000000ff ) |
                   ((x & (0x01ff0000 >> 16 )) <<
                    16 ));
}
static inline void G2_SetOBJShape (GXOamAttr * oam, GXOamShape shape)
{
    ((void) 0) ;
    oam->attr01 = ((oam->attr01 & ~(0x0000c000 | 0xc0000000 )) | shape);
}
static inline void G2_SetOBJCharName (GXOamAttr * oam, int name)
{
    ((void) 0) ;
    oam->attr2 = (u16)((oam->attr2 & ~0x03ff ) | name);
}
static inline void G2_SetOBJColorMode (GXOamAttr * oam, GXOamColorMode color)
{
    ((void) 0) ;
    ((void) 0)
                ;
    oam->attr01 = ((oam->attr01 & ~0x00002000 ) | (color << 13 ));
}
extern const u16 (*ctrdgi_fl_maxtime);
static inline u32 MATH_CountLeadingZerosInline (u32 x)
            {
                asm
                {
                    clz x, x
                }
                return x;
            }
static inline int MATH_ILog2(u32 x)
{
	return (int)(31 - MATH_CountLeadingZerosInline(x) );
}
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
typedef enum NNSG2dOBJVramMode {
    NNS_G2D_OBJVRAMMODE_32K  = 0,
    NNS_G2D_OBJVRAMMODE_64K  = 1,
    NNS_G2D_OBJVRAMMODE_128K = 2,
    NNS_G2D_OBJVRAMMODE_256K = 3
} NNSG2dOBJVramMode;
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
int native_main_02036538(GXOamAttr * oam, int areaWidth, int areaHeight, int x, int y, GXOamColorMode color, int charName, NNSG2dOBJVramMode vramMode);
typedef struct ObjectSize {
    u8 widthShift;
    u8 heightShift;
} ObjectSize;
typedef struct {
unsigned char field_0000[4];
unsigned char field_0004[4];
unsigned char field_0008[4];
const NNSiG2dCharCanvasVTable field_000c;
const NNSiG2dCharCanvasVTable field_0018;
const NNSiG2dCharCanvasVTable field_0024;
const ObjectSize field_0030[4][4];
unsigned char field_0050[64];
} NativeStorage_020d90d0;
extern NativeStorage_020d90d0 native_data_main_020d90d0;
static inline const ObjectSize * GetMaxObjectSize (int w, int h)
{
    int log_w = (w >= 8) ? 3: MATH_ILog2((unsigned long)w);
    int log_h = (h >= 8) ? 3: MATH_ILog2((unsigned long)h);
    ((void) 0) ;
    ((void) 0) ;
    return &native_data_main_020d90d0.field_0030[log_h][log_w];
}
GXOamShape native_fn_02035634 (const ObjectSize * pSize);
