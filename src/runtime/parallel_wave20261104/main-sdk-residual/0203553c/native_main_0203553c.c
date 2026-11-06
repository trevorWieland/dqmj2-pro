#include "context.h"
u32 native_main_0203553c (u32 cx, u32 cy, u32 areaWidth, u32 areaHeight, u32 objWidth, u32 objHeight)
{
    const u32 fullbits = (u32)(~0);
    u32 idx = 0;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    for (;;) {
        const u32 objWidthMaskInv = fullbits << objWidth;
        const u32 objHeightMaskInv = fullbits << objHeight;
        const u32 areaAWidth = areaWidth & objWidthMaskInv;
        const u32 areaAHeight = areaHeight & objHeightMaskInv;
        if ( areaAHeight <= cy ) {
            idx += areaWidth * areaAHeight;
            if ( areaAWidth <= cx ) {
                idx += (areaHeight - areaAHeight) * areaAWidth;
                cx -= areaAWidth;
                cy -= areaAHeight;
                areaWidth -= areaAWidth;
                areaHeight -= areaAHeight;
            } else {
                cy -= areaAHeight;
                areaWidth = areaAWidth;
                areaHeight -= areaAHeight;
            }
        } else {
            const u32 objHeightMask = ~objHeightMaskInv;
            if ( areaAWidth <= cx ) {
                idx += (u32)(areaAWidth * areaAHeight);
                cx -= areaAWidth;
                areaWidth -= areaAWidth;
                areaHeight = areaAHeight;
            } else {
                const u32 objWidthMask = ~objWidthMaskInv;
                idx += (u32)(cy & objHeightMaskInv) * areaAWidth;
                idx += (u32)(cx & objWidthMaskInv) << objHeight;
                idx += (u32)(cy & objHeightMask) << objWidth;
                idx += (u32)(cx & objWidthMask);
                return idx;
            }
        }
        {
            const ObjectSize * pobj = GetMaxObjectSize((int)areaWidth, (int)areaHeight);
            objWidth = pobj->widthShift;
            objHeight = pobj->heightShift;
        }
    }
}
