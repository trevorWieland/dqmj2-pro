#include "selection_lines.h"

void native_main_02078cbc(void)
{
    SelectionPanel *panel = native_fn_ov000_02217440();
    u32 cursor = native_fn_ov000_022174f4();
    cursor += native_fn_02068de0(19, 0, panel->selector, 127, 8, 4, 1, cursor);
    cursor += native_fn_02068de0(20, 1, panel->selector, 127, 17, 4, 1, cursor);
    cursor += native_fn_02068f70(21, 0, panel->selector, 1, 6, 21, cursor, 5, 2, 11, 24, 1);
    cursor += native_fn_02068f70(22, 1, panel->selector, 1, 18, 21, cursor, 5, 2, 12, 20, 1);
    native_fn_ov000_02217500(cursor);
}
