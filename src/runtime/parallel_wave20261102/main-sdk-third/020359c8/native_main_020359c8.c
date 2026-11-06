#include "context_00.h"
void native_main_020359c8 (const NNSG2dCharCanvas * pCC, const NNSG2dFont * pFont, int x, int y, int cl, const NNSG2dGlyph * pGlyph)
{
    int ofs_x_base;
    int ofs_x;
    int ofs_y;
    int ofs_x_end;
    int ofs_y_end;
    unsigned int nextLineOffset;
    u8 * pChar;
    u8 glyphWidth;
    u8 charHeight;
    int charSize;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0)
                          ;
    charSize = GetCharacterSize(pCC);
    {
        int chara_x_num;
        int chara_y_num;
        const unsigned int areaWidth = (unsigned int)pCC->areaWidth;
        const unsigned int areaHeight = (unsigned int)pCC->areaHeight;
        u8 * const charBase = pCC->charBase;
        const NNSG2dCharWidths * const pWidth = pGlyph->pWidths;
        unsigned int chara_x_begin;
        unsigned int chara_x_last;
        unsigned int chara_y_begin;
        unsigned int chara_y_last;
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
        pChar = charBase + (pCC->param * chara_y_begin + chara_x_begin) * charSize;
        nextLineOffset = (pCC->param - chara_x_num) * charSize;
        ofs_x_base = (x < 0) ? x: x & 0x7;
        ofs_y = (y < 0) ? y: y & 0x7;
        ofs_x_end = ofs_x_base - 8 * chara_x_num;
        ofs_y_end = ofs_y - 8 * chara_y_num;
    }
    {
        LC_INFO i;
        i.src = pGlyph->image;
        i.width = glyphWidth;
        i.height = charHeight;
        i.cl = (u32)(cl - 1);
        i.srcBpp = NNS_G2dFontGetBpp(pFont);
        i.dstBpp = pCC->dstBpp;
        i.dsrc = NNS_G2dFontGetCellWidth(pFont) * i.srcBpp;
        for ( ; ofs_y > ofs_y_end; ofs_y -= 8 ) {
            i.ofs_y = ofs_y;
            for (ofs_x = ofs_x_base; ofs_x > ofs_x_end; ofs_x -= 8 ) {
                i.dst = pChar;
                i.ofs_x = ofs_x;
                native_fn_02035788(&i);
                pChar += charSize;
            }
            pChar += nextLineOffset;
        }
    }
}
