#include "context_00.h"
void native_main_02037330 (const NNSG2dTextCanvas * pTxn, int x, int y, int cl, const void * str, const void ** pPos
                                   , NNSiG2dTextDirection d
                                   )
{
    const void * pos;
    int charSpace;
    const NNSG2dFont * pFont;
    u16 c;
    NNSiG2dSplitCharCallback getNextChar;
    ((void) 0) ;
    ((void) 0); ;
    ((void) 0)
                   ;
    ((void) 0)
                          ;
    charSpace = pTxn->hSpace;
    pFont = pTxn->pFont;
    pos = str;
    getNextChar = NNSi_G2dFontGetSpliter(pFont);
    while ((c = getNextChar((const void **)&pos)) != 0) {
        if (c == '\n') {
            break;
        }
        {
            const int w = native_fn_020361f8(pTxn->pCanvas, pFont, x, y, cl, c) + charSpace;
            x += w * d.x;
            y += w * d.y;
        }
    }
    if (pPos != ((void *)0) ) {
        *pPos = (c == '\n') ? pos: ((void *)0) ;
    }
}
