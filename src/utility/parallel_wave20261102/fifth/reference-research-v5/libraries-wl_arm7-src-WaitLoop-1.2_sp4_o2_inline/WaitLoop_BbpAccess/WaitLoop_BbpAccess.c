#include "context000.h"

u32 WaitLoop_BbpAccess(void)
{
    u32 i;
    for (i = 0; i < 10240; i++) {
        if ((*(vu16 *)(0x04808000 + 0x15E) & (0x0001 << 0) ) == 0) {
            return 0;
        }
    }
    ;
    return 1;
}
