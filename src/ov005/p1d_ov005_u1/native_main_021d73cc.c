#include "context.h"

/* Table+0x18 dispatcher: forward the wrapper's first two arguments to the
   slot; the third register argument is not part of the callback contract. */
void native_main_021d73cc(void *self, u32 a, u32 b, u32 c)
{
    Ov005Interface *iface = *(Ov005Interface **)((u8 *)self + 0x20);
    void (*callback)(void *, u32, u32) =
        *(void (**)(void *, u32, u32))((u8 *)iface->table + 0x18);

    callback(self, a, b);
}
