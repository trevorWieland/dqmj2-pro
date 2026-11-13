#include "context.h"
void native_main_02073090(s32 option)
{
    void *object=ov000_display_context_02215698();
    u8 *state=(u8 *)&native_data_021c5b20;
    native_fn_ov000_022162c0(native_fn_02049ad0(1));
    native_fn_ov000_02216664(state);
    native_fn_0204b61c((u8 *)object+16,0);
    native_fn_020756e4(0,-1,-1);
    if(native_fn_02062378()!=0)native_fn_020619b0(0);
    native_fn_ov000_022162c0(native_fn_02049ad0(24));
    native_fn_ov000_022162c0(native_fn_02049ad0(25));
    native_fn_ov000_022162c0(native_fn_02049ad0(27));
    native_fn_ov000_022162c0(native_fn_02049ad0(28));
    native_fn_ov000_02215078(state+0xa8,1);
    if(option!=0)native_fn_ov000_021e7b9c(83);
}
