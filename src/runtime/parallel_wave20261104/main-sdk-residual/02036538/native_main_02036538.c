#include "context.h"
int native_main_02036538 (GXOamAttr * oam, int areaWidth, int areaHeight, int x, int y, GXOamColorMode color, int charName, NNSG2dOBJVramMode vramMode)
{
    const u32 fullbits = (u32)(~0);
    const ObjectSize * pSize = GetMaxObjectSize(areaWidth, areaHeight);
    const int objWidthShift = pSize->widthShift;
    const int objHeightShift = pSize->heightShift;
    const u32 objWidthMaskInv = fullbits << objWidthShift;
    const u32 objHeightMaskInv = fullbits << objHeightShift;
    const u32 areaAWidth = areaWidth & objWidthMaskInv;
    const u32 areaAHeight = areaHeight & objHeightMaskInv;
    const int charNameUnit = (color == GX_OAM_COLORMODE_16) ? 1: 2;
    int usedObjs = 0;
    ((void) 0); ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    {
        const GXOamShape shape = native_fn_02035634(pSize);
        const int xNum = areaWidth >> objWidthShift;
        const int yNum = areaHeight >> objHeightShift;
        const int charNameSize = ((charNameUnit << objWidthShift) << objHeightShift) >> vramMode;
        int ox, oy;
        for (oy = 0; oy < yNum; ++oy) {
            const int py = y + (oy << objHeightShift) * 8 ;
            for (ox = 0; ox < xNum; ++ox) {
                const int px = x + (ox << objWidthShift) * 8 ;
                G2_SetOBJPosition(oam, px, py);
                G2_SetOBJShape(oam, shape);
                G2_SetOBJCharName(oam, charName);
                G2_SetOBJColorMode(oam, color);
                oam++;
                charName += charNameSize;
            }
        }
        usedObjs += xNum * yNum;
    }
    if ( areaAWidth < areaWidth ) {
        const unsigned int areaBWidth = areaWidth - areaAWidth;
        const unsigned int areaBHeight = areaAHeight;
        const int px = x + (int)areaAWidth * 8 ;
        const int py = y;
        const int areaBObjs = native_main_02036538(oam, (int)areaBWidth, (int)areaBHeight, px, py, color, charName, vramMode);
        oam += areaBObjs;
        usedObjs += areaBObjs;
        charName += (charNameUnit * areaBWidth * areaBHeight) >> vramMode;
    }
    if ( areaAHeight < areaHeight ) {
        const unsigned int areaCWidth = areaAWidth;
        const unsigned int areaCHeight = areaHeight - areaAHeight;
        const int px = x;
        const int py = y + (int)areaAHeight * 8 ;
        const int areaCObjs = native_main_02036538(oam, (int)areaCWidth, (int)areaCHeight, px, py, color, charName, vramMode);
        oam += areaCObjs;
        usedObjs += areaCObjs;
        charName += (charNameUnit * areaCWidth * areaCHeight) >> vramMode;
    }
    if ( areaAWidth < areaWidth && areaAHeight < areaHeight ) {
        const unsigned int areaDWidth = areaWidth - areaAWidth;
        const unsigned int areaDHeight = areaHeight - areaAHeight;
        const int px = x + (int)areaAWidth * 8 ;
        const int py = y + (int)areaAHeight * 8 ;
        const int areaDObjs = native_main_02036538(oam, (int)areaDWidth, (int)areaDHeight, px, py, color, charName, vramMode);
        usedObjs += areaDObjs;
    }
    return usedObjs;
}
