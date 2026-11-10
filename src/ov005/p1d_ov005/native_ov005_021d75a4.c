#include "context.h"

/* Table+0x0c dispatcher that tolerates a cleared slot. */
void native_ov005_021d75a4(void *self, u32 a, u32 b)
{
    Ov005Interface *iface = *(Ov005Interface **)((u8 *)self + 0x20);
    void (*callback)(void *, u32, u32) =
        *(void (**)(void *, u32, u32))((u8 *)iface->table + 0x0c);

    if (callback == 0)
        return;
    callback(self, a, b);
}

