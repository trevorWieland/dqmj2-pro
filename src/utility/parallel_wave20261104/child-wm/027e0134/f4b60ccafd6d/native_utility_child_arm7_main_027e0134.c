#include "dependency000.h"

u32 *native_utility_child_arm7_main_027e0134(void)
{
    s32 i;
    u32 *ret = ((void *)0) ;
    OSIntrMode e;
    e = native_utility_child_arm7_arm_037fe41c();
    if (native_utility_child_arm7_data_027f84f0.wm7buf != ((void *)0) ) {
        for (i = 0; i < 32; i++) {
            if (native_utility_child_arm7_data_027f84f0.wm7buf->requestBuf[i * 4] & 0x8000 ) {
                ret = &(native_utility_child_arm7_data_027f84f0.wm7buf->requestBuf[i * 4]);
                *ret &= ~(0x8000 );
                break;
            }
        }
    }
    (void)native_utility_child_arm7_arm_037fe430(e);
    return ret;
}
