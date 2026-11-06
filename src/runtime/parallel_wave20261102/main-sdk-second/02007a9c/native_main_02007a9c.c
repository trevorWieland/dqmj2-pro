#include "context_00.h"
OSTick native_main_02007a9c (void)
{
    vu16 countL;
    vu64 countH;
    OSIntrMode prev = native_fn_02007ff4();
    ((void) 0) ;
    countL = *(REGType16 *)((u32)(0x04000000 + 0x100) + OS_TIMER_0 * 4);
    countH = native_data_main_020e36f4.field_0008 & 0xffffffffffffULL;
    if ((*( REGType32v *) (0x04000000 + 0x214)) & (1UL << 3) && !(countL & 0x8000)) {
        countH++;
    }
    (void)native_fn_02008008(prev);
    return (countH << 16) | countL;
}
