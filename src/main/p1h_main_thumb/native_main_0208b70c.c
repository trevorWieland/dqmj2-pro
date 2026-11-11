#include "context.h"

extern void native_fn_02006924(void);

/* Count down the live window and release it when it expires. */
void native_main_0208b70c(u8 *window)
{
    if (*(u32 *)(window + 0x08) == 0x01ff8000) {
        u32 remaining = *(u32 *)(window + 0x0c) - 1;

        *(u32 *)(window + 0x0c) = remaining;
        if (remaining == 0) {
            *(u32 *)(window + 0x08) = 0;
            native_fn_02006924();
        }
    }
}
