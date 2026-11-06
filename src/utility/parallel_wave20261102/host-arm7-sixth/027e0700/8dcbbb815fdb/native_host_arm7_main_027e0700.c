#include "dependency000.h"

u32 *native_host_arm7_main_027e0700(void)
{
    s32 i;
    u32 *ret = ((void *)0) ;
    OSIntrMode e;
    e = native_host_arm7_arm_037fdd00();
    if (native_host_arm7_data_027f7884.wm7buf != ((void *)0) ) {
        for (i = 0; i < 32; i++) {
            if (native_host_arm7_data_027f7884.wm7buf->requestBuf[i * 4] & 0x8000 ) {
                ret = &(native_host_arm7_data_027f7884.wm7buf->requestBuf[i * 4]);
                *ret &= ~(0x8000 );
                break;
            }
        }
    }
    (void)native_host_arm7_arm_037fdd14(e);
    return ret;
}
