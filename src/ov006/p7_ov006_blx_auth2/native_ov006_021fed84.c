#include "context.h"

/* 0x0221C148 holds the handle allocated here. */
extern u32 native_data_ov006_0221c148;

extern u32 native_ov006_02203c08(s32 id, s32 size);
extern void native_fn_02019a58(u32 address, u32 value);
extern void native_fn_020a47cc(u32 handle);

/* ov006 row 0x021FED84: 52 bytes. Allocate 0x20 bytes of resource 0x6F8, save
   the handle in the shared slot, program two words into the block 0x4F8 bytes
   past it, then release the handle that is now in the slot. The call at +0x06
   is a Thumb BL into the overlay; the call at +0x14 targets ARM code and is a
   BLX immediate in the image (1A F6 5E EE). Unknown: the meaning of the
   resource id and of the (address, value) pair 0x4F8/0xA001, and the ARM
   callees' semantics, which are inferred only from the call shape. */
void native_ov006_021fed84(void)
{
    u32 handle = native_ov006_02203c08(0x6F8, 0x20);

    native_data_ov006_0221c148 = handle;
    native_fn_02019a58(handle + 0x4F8, 0xA001);
    native_fn_020a47cc(native_data_ov006_0221c148);
}
