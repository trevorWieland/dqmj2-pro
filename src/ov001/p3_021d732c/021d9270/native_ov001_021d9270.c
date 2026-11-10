#include "../context.h"

/* Clears the 84-byte mixer block at 0x02235530 (four 20-byte slots) and resets
   every slot through 0x020286e8, then flushes the whole group through the mixer
   selector 0x021d92f8 with the slot count and a zero mode. */
u32 native_ov001_021d9270(void) {
    u32 slot;
    s32 index;

    native_fn_02008d78(native_data_ov001_02235530, 0, 84);
    slot = 0;
    index = 0;
    do {
        native_fn_020286e8(native_data_ov001_02235534 + slot, index & 0xFF);
        index++;
        slot += 20;
    } while (index < 4);
    return native_fn_ov001_021d92f8(index, 0);
}
