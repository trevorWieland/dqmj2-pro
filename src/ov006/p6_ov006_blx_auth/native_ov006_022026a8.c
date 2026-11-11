#include "context.h"

/* 0x0221C16C holds the pointer to a 0x100-byte buffer; the second 0x100 bytes
   behind it and the pointer word at +0xAB0 inside it are reset here. The
   measured code re-reads the pointer for every access, so the source does not
   keep a local copy. */
extern u32 native_data_ov006_0221c16c;

extern void native_fn_02008d78(void *dst, s32 value, u32 size);

/* ov006 row 0x022026A8: 48 bytes. Clear the second half of the buffer, clear
   the first half, then store the buffer pointer back into its own +0xAB0 word.
   Both calls at +0x0E and +0x1E target ARM code and are BLX immediates in the
   image (06 F6 60 EB / 06 F6 58 EB). Unknown: why the reset writes the pointer
   into its own buffer and what consumes that word. */
void native_ov006_022026a8(void)
{
    native_fn_02008d78((u8 *)native_data_ov006_0221c16c + 0x100, 0, 0x100);
    native_fn_02008d78((u8 *)native_data_ov006_0221c16c, 0, 0x100);
    *(u32 *)((u8 *)native_data_ov006_0221c16c + 0xAB0) = native_data_ov006_0221c16c;
}
