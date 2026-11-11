#include "context.h"

/* 0x0221C144 is a main-side state slot. The measured literal pool carries its
   address twice, i.e. the original reachable it through two distinct object
   symbols: a scalar read for the gate and an address pass-through for the
   handler. Both names below denote that one address. */
extern u32 native_data_ov006_0221c144;
extern u8 native_data_ov006_alias_0221c144[];

extern s32 native_fn_02012290(void);
extern void native_ov006_02203c20(u32 *state);

/* ov006 row 0x021FEA78: 40 bytes. If the state word at 0x0221C144 is set, spin
   on native_fn_02012290 until it returns 0x8000, then hand the state slot's
   address to native_ov006_02203C20. The call at +0x0E targets ARM code and is a
   BLX immediate in the image (13 F6 04 EC); the call at +0x18 is a Thumb BL into
   the overlay. Unknown: what native_fn_02012290 polls and why 0x8000 terminates
   the wait. */
void native_ov006_021fea78(void)
{
    if (native_data_ov006_0221c144 == 0)
        return;

    while (native_fn_02012290() != 0x8000)
        ;

    native_ov006_02203c20((u32 *)native_data_ov006_alias_0221c144);
}
