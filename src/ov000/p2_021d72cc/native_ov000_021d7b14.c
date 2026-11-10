#include "context.h"

/* Slot 0x21d7b14: hand the selected table entry to two subsystem callbacks. */
void native_ov000_021d7b14(s32 index, s32 value, s32 mode)
{
    native_fn_02049ffc(native_data_ov000_022300f8[index]);
    native_fn_02087a48(native_data_ov000_022300f8[index], 0, mode, 0, 1, value);
}
