#include "context.h"

/* 0x0221C134 holds a pointer to the shared 0x608-byte block: the word at +0x00
   of that block is the block's own owner handle and +0x04 starts the
   0x600-byte payload this row fills. */
extern u32 native_data_ov006_0221c134;

extern u32 native_ov006_02203c08(s32 id, s32 size);
extern void native_fn_02008ca4(u32 first, u32 second, s32 size);
extern u32 native_ov006_0220490c(s32 which, void *callback, s32 arg2, s32 arg3);
/* Address taken as data so mwcc folds the Thumb bit into the relocation. */
extern u8 native_ov006_021fe544[];

/* ov006 row 0x021FE49C: 64 bytes. Allocate the shared block, publish the owner
   handle, copy the 0x600-byte payload into it from the caller's buffer, then
   arm the release callback 0x021FE544 for 0x78 frames and store that frame
   token through the owner handle. The call at +0x1A targets ARM code and is a
   BLX immediate in the image (0A F6 F6 EB). Unknown: what the owner word at
   +0x00 is used for elsewhere, and the meaning of the "0x608"/4 allocation
   pair; the copy helper's direction is inferred from the image's argument
   order (source first, destination second). */
void native_ov006_021fe49c(u32 source)
{
    u32 handle = native_ov006_02203c08(0x608, 4);

    native_data_ov006_0221c134 = handle;
    native_fn_02008ca4(source, handle + 4, 0x600);
    *(u32 *)native_data_ov006_0221c134 =
        native_ov006_0220490c(1, (void *)(native_ov006_021fe544 + 1), 0, 0x78);
}
