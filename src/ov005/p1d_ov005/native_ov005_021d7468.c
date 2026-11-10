#include "context.h"

/* Table+0x04 dispatcher: forward the wrapper's first argument to the slot. */
void native_ov005_021d7468(void *self, u32 a, u32 b)
{
    Ov005Interface *iface = *(Ov005Interface **)((u8 *)self + 0x20);
    void (*callback)(void *, u32) =
        *(void (**)(void *, u32))((u8 *)iface->table + 0x04);

    callback(self, a);
}

