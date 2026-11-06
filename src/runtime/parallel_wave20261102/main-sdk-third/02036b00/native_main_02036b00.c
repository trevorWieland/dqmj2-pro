#include "context_00.h"
NNSG2dTextRect native_main_02036b00 (const NNSG2dFont * pFont, int hSpace, int vSpace, const void * txt)
{
    int lines = 1;
    NNSG2dTextRect rect = {0, 0};
    ((void) 0) ;
    ((void) 0); ;
    while (txt != ((void *)0) ) {
        const int width = native_fn_020369e0(pFont, hSpace, txt, &txt);
        if (width > rect.width) {
            rect.width = width;
        }
        lines++;
    }
    rect.height = ((lines - 1) * (NNS_G2dFontGetLineFeed(pFont) + vSpace) - vSpace);
    return rect;
}
