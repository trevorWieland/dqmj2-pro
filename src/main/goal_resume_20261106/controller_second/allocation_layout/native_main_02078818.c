#include "allocation_layout.h"

void native_main_02078818(const Selection *selection)
{
    void *display = native_fn_ov000_02215698();
    Point point = {0, 0};
    switch (native_data_021c6234) {
    case 0:
    case 1:
        point.x = 16;
        point.y = 40;
        break;
    case 2:
    case 3:
        point.x = 16;
        point.y = 48;
        break;
    default:
        return;
    }
    point.y += (selection->selected - selection->scroll) * 16;
    native_fn_0204b53c((LayoutState *)((u8 *)display + 16), &point);
}
