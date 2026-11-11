#include "context.h"

/* 0x0221C1A4 is a two-word main-side descriptor shared with
   native_ov006_022041f0: word 0 is the table pointer handed to the dispatch
   helper, word 1 the handle shut down by the close helper. */
struct native_descriptor_0221c1a4 {
    u32 table;
    u32 handle;
};

extern struct native_descriptor_0221c1a4 native_data_ov006_0221c1a4;

extern void native_fn_02005cf4(u32 handle);
extern void native_fn_02005d20(s32 key);
extern u32 native_fn_02005bd8(s32 mode);
extern void native_fn_02005b50(s32 mode, u32 table);
extern void native_fn_02005d80(s32 mode);
extern void native_fn_02007fe0(void);
/* Address taken as data so mwcc folds the Thumb bit into the relocation. */
extern u8 native_ov006_02204218[];

/* ov006 row 0x022041A0: 80 bytes. Bring the subsystem up opposite to
   native_ov006_022041f0: latch the current 0x04000210 word as the descriptor's
   handle, hand 0x00040018 to the restore helper, release the shared lock, build
   the descriptor's table from mode 1 of 0x02005BD8, install callback
   0x02204219, dispatch mode 1 again, enable interrupts and notify. Calls at
   +0x0C, +0x12, +0x18, +0x22, +0x28 and +0x36 target ARM code and are BLX
   immediates in the image. Unknown: the descriptor's real field names, what
   0x00040018 is, and why the interrupt-mask read before the enable is dead but
   volatile in the measured code. */
void native_ov006_022041a0(void)
{
    u32 handle = *(volatile u32 *)0x04000210;

    native_data_ov006_0221c1a4.handle = handle;

    native_fn_02005cf4(0x00040018);
    native_fn_02005d20(1);
    native_data_ov006_0221c1a4.table = native_fn_02005bd8(1);
    native_fn_02005b50(1, (u32)(native_ov006_02204218 + 1));
    native_fn_02005d80(1);

    {
        u16 mask = *(volatile u16 *)0x04000208;
        (void)mask;
        *(volatile u16 *)0x04000208 = 1;
    }
    native_fn_02007fe0();
}
