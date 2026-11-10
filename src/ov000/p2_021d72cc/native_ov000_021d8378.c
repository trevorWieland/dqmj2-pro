#include "context.h"

/* Sample the motion solver and fold its result into the controller's position
   slots. The helper fills the frame, the second seeds it with the live value,
   and the third resolves the frame's 0x24/0x30 sub-blocks. */
void native_ov000_021d8378(void)
{
    SampleFrame frame;
    s32 y;

    frame.field_30 = 0;
    frame.field_34 = 0;
    frame.field_38 = native_data_ov000_0223033c.field_50;
    native_fn_02000ce8(&frame);
    native_fn_02028044(&frame, native_data_ov000_0223033c.field_4c);
    native_fn_0200103c(&frame.field_30, &frame, &frame.field_24);
    native_data_ov000_0223033c.field_74 = frame.field_24 + native_data_ov000_0223033c.field_68;
    y = frame.field_28 + native_data_ov000_0223033c.field_6c;
    native_data_ov000_0223033c.field_78 = y;
    native_data_ov000_0223033c.field_7c = frame.field_2c + native_data_ov000_0223033c.field_70;
    native_data_ov000_0223033c.field_78 = y + native_data_ov000_0223033c.field_54;
}
