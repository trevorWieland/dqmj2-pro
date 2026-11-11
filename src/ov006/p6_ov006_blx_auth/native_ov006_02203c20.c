#include "context.h"

/* 0x0221C188 holds the main-side slot pointer. The caller keeps its own handle
   in the word it points at; the slot copy is the value released here. */
extern u32 native_data_ov006_0221c188;

extern s32 native_fn_02005d50(s32 lock);
extern void native_fn_02005d20(s32 key);
extern void native_fn_0202b4e8(u32 slot, s32 value);

/* ov006 row 0x02203C20: 44 bytes. Under the shared lock, release the main-side
   slot for the handle's current value, drop the lock and clear the handle. A
   zero handle skips the whole body (including the release). Calls at +0x06 and
   +0x1A target ARM code and are BLX immediates in the image
   (02 F6 94 E8 / 02 F6 70 E8); the release call at +0x16 is a BLX immediate
   (27 F6 58 EC). Unknown: what the slot is and why the zero path skips the
   release. */
void native_ov006_02203c20(s32 *handle)
{
    s32 key = native_fn_02005d50(1);

    if (*handle != 0) {
        native_fn_0202b4e8(native_data_ov006_0221c188, *handle);
        native_fn_02005d20(key);
        *handle = 0;
    }
}
