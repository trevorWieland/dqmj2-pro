#include "context.h"

/* Switch the scene layout: release the previous layout buffer, hand the new
   layout its work buffer, and reprogram the background mode, the BG2 priority
   field and the rotation parameters. */
void native_ov006_021da4f0(s32 layout)
{
    u32 *regs = (u32 *)0x04000000;

    if (layout != -1) {
        if (native_data_ov006_0220f33c.field_08 != 0) {
            native_fn_020bb38c(native_data_ov006_0220f33c.field_08, 1);
            native_data_ov006_0220f33c.field_08 = 0;
        }
        native_fn_ov006_021da3e8(layout);
        native_fn_02004d98(native_data_ov006_0220f33c.field_08 + 8, 0, 0x18000);
    } else {
        native_fn_02004d98(native_data_ov006_0220f33c.field_08, 0, 0x18000);
    }
    regs[0] = (regs[0] & ~0x1f00) | 0x1800;
    *(u16 *)((u8 *)regs + 0x0e) = *(u16 *)((u8 *)regs + 0x0e) & ~3;
    regs[7] = 0;
    native_fn_020bb38c(native_data_ov006_0220f33c.field_08, 1);
    native_data_ov006_0220f33c.field_08 = 0;
}
