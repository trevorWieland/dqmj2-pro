#include "context_00.h"
void native_main_02035b60 (const NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, const NNSG2dGlyph * pGlyph)
{
    int ofs_x_base;
    int ofs_x;
    int ofs_y;
    int ofs_x_end;
    int ofs_y_end;
    int cx, cx_base;
    int cy;
    u8 glyphWidth;
    u8 charHeight;
    int charSize;
    u16 * mapTable;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0)
                          ;
    charSize = GetCharacterSize(pCC);
    mapTable = (u16 *)(pCC->param);
    {
        int chara_x_num;
        int chara_y_num;
        const unsigned int areaWidth = (unsigned int)pCC->areaWidth;
        const unsigned int areaHeight = (unsigned int)pCC->areaHeight;
        const NNSG2dCharWidths * const pWidth = pGlyph->pWidths;
        u32 chara_x_begin;
        u32 chara_x_last;
        u32 chara_y_begin;
        u32 chara_y_last;
        glyphWidth = pWidth->glyphWidth;
        charHeight = NNS_G2dFontGetCellHeight(pFont);
        if ( glyphWidth <= 0 ) {
            return;
        }
        if ((x + glyphWidth < 0) || (y + charHeight) < 0 ) {
            return;
        }
        chara_x_begin = (x <= 0) ? 0: ((u32)x / 8 );
        chara_y_begin = (y <= 0) ? 0: ((u32)y / 8 );
        chara_x_last = (u32)(x + glyphWidth + (8 - 1)) / 8 ;
        if ( chara_x_last >= areaWidth ) {
            chara_x_last = areaWidth;
        }
        chara_y_last = (u32)(y + charHeight + (8 - 1)) / 8 ;
        if ( chara_y_last >= areaHeight ) {
            chara_y_last = areaHeight;
        }
        chara_x_num = (int)(chara_x_last - chara_x_begin);
        chara_y_num = (int)(chara_y_last - chara_y_begin);
        if ((chara_x_num < 0) || (chara_y_num < 0)) {
            return;
        }
        cx_base = (int)chara_x_begin;
        cy = (int)chara_y_begin;
        ofs_x_base = (x < 0) ? x: x & 0x7;
        ofs_y = (y < 0) ? y: y & 0x7;
        ofs_x_end = ofs_x_base - 8 * chara_x_num;
        ofs_y_end = ofs_y - 8 * chara_y_num;
    }
    {
        LC_INFO i;
        u8 * const pCharBase = pCC->charBase;
        OBJ1DParam p;
        i.src = pGlyph->image;
        i.width = glyphWidth;
        i.height = charHeight;
        i.cl = (u32)(cl - 1);
        i.srcBpp = NNS_G2dFontGetBpp(pFont);
        i.dstBpp = pCC->dstBpp;
        i.dsrc = NNS_G2dFontGetCellWidth(pFont) * i.srcBpp;
        p.packed = pCC->param;
        {
            const u32 areaWidth = (u32)pCC->areaWidth;
            const u32 areaHeight = (u32)pCC->areaHeight;
            const u32 baseWidthShift = p.baseWidthShift;
            const u32 baseHeightShift = p.baseHeightShift;
            for ( ; ofs_y > ofs_y_end; ofs_y -= 8 ) {
                i.ofs_y = ofs_y;
                cx = cx_base;
                for (ofs_x = ofs_x_base; ofs_x > ofs_x_end; ofs_x -= 8 ) {
                    const unsigned int iChar = native_fn_0203553c((u32)cx, (u32)cy, areaWidth, areaHeight, baseWidthShift, baseHeightShift);
                    i.ofs_x = ofs_x;
                    i.dst = pCharBase + iChar * charSize;
                    native_fn_02035788(&i);
                    cx++;
                }
                cy++;
            }
        }
    }
}
