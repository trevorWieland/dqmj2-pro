#include "context_00.h"
void native_main_020373e4 (const NNSG2dTextCanvas * pTxn, int x, int y, int areaWidth, int cl, u32 flags, const void * txt
                                      , NNSiG2dTextDirection d
                                      )
{
    const void * str;
    int linefeed;
    int linefeedx;
    int linefeedy;
    int line;
    int charSpace;
    const NNSG2dFont * pFont;
    int px, py;
    ((void) 0) ;
    ((void) 0); ;
    ((void) 0)
                   ;
    ((void) 0)
                          ;
    charSpace = pTxn->hSpace;
    linefeed = NNS_G2dFontGetLineFeed(pTxn->pFont) + pTxn->vSpace;
    pFont = pTxn->pFont;
    str = txt;
    linefeedx = linefeed * -d.y;
    linefeedy = linefeed * d.x;
    line = 0;
    while (str != ((void *)0) ) {
        px = x + line * linefeedx;
        py = y + line * linefeedy;
        if (flags & NNS_G2D_HORIZONTALALIGN_RIGHT) {
            const int width = NNS_G2dTextCanvasGetStringWidth(pTxn, str, ((void *)0) );
            const int offset = areaWidth - width;
            px += offset * d.x;
            py += offset * d.y;
        } else if (flags & NNS_G2D_HORIZONTALALIGN_CENTER)   {
            const int width = NNS_G2dTextCanvasGetStringWidth(pTxn, str, ((void *)0) );
            const int offset = (areaWidth + 1) / 2 - (width + 1) / 2;
            px += offset * d.x;
            py += offset * d.y;
        }
        native_fn_02037330(pTxn, px, py, cl, str, &str, d);
        line++;
    }
}
