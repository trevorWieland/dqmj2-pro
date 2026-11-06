#include "context000.h"

static void WlIntrCntOvf(void) __attribute__((never_inline))
{
    ;
    ;
    WUpdateCounter();
    ;
    *(vu16 *)((0x04808000) + 0x1AC) = 0xFFFF;
    *(vu16 *)((0x04808000) + 0x010) = (0x0003 << 4) ;
}
