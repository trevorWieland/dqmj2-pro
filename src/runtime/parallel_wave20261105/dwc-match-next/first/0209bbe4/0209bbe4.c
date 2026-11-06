#include "context.h"
u8 native_main_0209bbe4(void)
{
    if (!stpDwcCnt) return 0;
    return stpDwcCnt->aid;
}