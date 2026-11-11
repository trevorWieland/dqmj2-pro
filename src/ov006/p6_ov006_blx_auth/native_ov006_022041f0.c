#include "context.h"

/* 0x0221C1A4 is a two-word main-side descriptor: word 0 is a table pointer
   passed to the restore helper, word 1 the pointer shut down first. */
struct native_descriptor_0221c1a4 {
    u32 table;
    u32 handle;
};

extern struct native_descriptor_0221c1a4 native_data_ov006_0221c1a4;

extern void native_fn_02005cf4(u32 handle);
extern void native_fn_02005b50(s32 mode, u32 table);

/* ov006 row 0x022041F0: 40 bytes. Shut down the subsystem: mask interrupts,
   close the descriptor's second word, then dispatch mode 1 with its first word.
   Calls at +0x0E and +0x18 target ARM code and are BLX immediates in the image
   (01 F6 7A ED / 01 F6 A2 EC). Unknown: the descriptor's real field names; the
   interrupt-mask read is dead but volatile in the measured code, so the source
   keeps it. */
void native_ov006_022041f0(void)
{
    u16 mask = *(volatile u16 *)0x04000208;
    (void)mask;
    *(volatile u16 *)0x04000208 = 0;

    native_fn_02005cf4(native_data_ov006_0221c1a4.handle);
    native_fn_02005b50(1, native_data_ov006_0221c1a4.table);
}
