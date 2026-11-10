#include "context.h"

/* Table+0x1c dispatcher: forward the wrapper's five arguments to the slot. */
void native_ov005_021d73e4(void *self, u32 a, u32 b, u32 c, u32 e)
{
    Ov005Interface *iface = *(Ov005Interface **)((u8 *)self + 0x20);
    void (*callback)(void *, u32, u32, u32, u32) =
        *(void (**)(void *, u32, u32, u32, u32))((u8 *)iface->table + 0x1c);

    callback(self, a, b, c, e);
}

