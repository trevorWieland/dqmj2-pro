#include "allocation_close.h"

void native_main_020771d4(u32 confirmed)
{
    void *display = native_fn_ov000_02215698();
    SelectionList *selection = &native_data_021c6234.skill_selection;
    if (native_data_021c6234.close_mode == 0) {
        native_data_021c6234.state = 0;
        native_fn_0204b61c((LayoutState *)((u8 *)display + 16), 0);
        native_fn_020620e8(1, 1);
        native_fn_ov000_022162c0(native_fn_02049ad0(24));
        native_fn_ov000_022162c0(native_fn_02049ad0(1));
        native_fn_ov000_02216664(selection);
        native_fn_ov000_021e7b9c(confirmed ? 0x52 : 0x53);
    } else if (native_data_021c6234.close_mode == 1) {
        native_fn_ov000_0221570c(confirmed);
        native_data_021c6234.state = 11;
    }
}
