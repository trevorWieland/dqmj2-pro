#include "context_00.h"
int native_main_020361f8 (const NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, u16 ccode)
{
    NNSG2dGlyph glyph;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0)
                          ;
    NNS_G2dFontGetGlyph(&glyph, pFont, ccode);
    switch (NNS_G2dFontGetFlags(pFont)) {
    case (NNS_G2D_FONT_FLAG_ROT_0):
    case (NNS_G2D_FONT_FLAG_ROT_270 | NNS_G2D_FONT_FLAG_TBRL):
    x += glyph.pWidths->left;
    break;
    case (NNS_G2D_FONT_FLAG_ROT_90):
    case (NNS_G2D_FONT_FLAG_ROT_0 | NNS_G2D_FONT_FLAG_TBRL):
        x -= NNS_G2dFontGetCellWidth(pFont);
        y += glyph.pWidths->left;
        break;
    case (NNS_G2D_FONT_FLAG_ROT_180):
    case (NNS_G2D_FONT_FLAG_ROT_90 | NNS_G2D_FONT_FLAG_TBRL):
        x -= glyph.pWidths->left + glyph.pWidths->glyphWidth;
        y -= NNS_G2dFontGetCellHeight(pFont);
        break;
    case (NNS_G2D_FONT_FLAG_ROT_270):
    case (NNS_G2D_FONT_FLAG_ROT_180 | NNS_G2D_FONT_FLAG_TBRL):
        y -= glyph.pWidths->left + NNS_G2dFontGetCellHeight(pFont);
        break;
}
    NNS_G2dCharCanvasDrawGlyph(pCC, pFont, x, y, cl, &glyph);
    return glyph.pWidths->charWidth;
}
