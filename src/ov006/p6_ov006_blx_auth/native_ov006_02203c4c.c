#include "context.h"

/* 0x0221C188 holds the main-side slot pointer that native_fn_0202B4E8 writes. */
extern u32 native_data_ov006_0221c188;

extern s32 native_fn_02005d50(s32 lock);
extern void native_fn_02005d20(s32 key);
extern void native_fn_0202b4e8(u32 slot, s32 value);

/* ov006 row 0x02203C4C: 40 bytes. Under the shared lock, push a non-zero value
   into the slot at 0x0221C188 and release the lock; a zero value returns
   without touching the slot (and without releasing — the measured code branches
   straight to the epilogue). Calls at +0x06 and +0x1A target ARM code and are
   BLX immediates in the image (02 F6 7E E8 / 02 F6 5A E8). The call at +0x16 is
   a BLX through the unresolved main symbol 0x0202B4E8. Unknown: what the slot
   is and why the zero path skips the release. */
void native_ov006_02203c4c(s32 value)
{
    s32 key = native_fn_02005d50(1);

    if (value != 0) {
        native_fn_0202b4e8(native_data_ov006_0221c188, value);
        native_fn_02005d20(key);
    }
}
