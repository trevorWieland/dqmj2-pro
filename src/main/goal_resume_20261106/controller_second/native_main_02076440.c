#include "layout_position.h"
void native_main_02076440(const Selection *selection) {
    Point point;
    u32 context = ov000_display_context_02215698();
    point.x = 16;
    switch (native_data_021c5a24.state) {
    case 0:
    case 1:
        point.y = 64;
        break;
    case 2:
    case 3:
        point.y = native_data_021c5a24.restricted_actions ? 48 : 64;
        break;
    case 5:
    case 6:
        point.y = 80;
        break;
    case 7:
    case 8:
        point.y = 80;
        break;
    default:
    case 4:
        return;
    }
    point.y += (selection->selected - selection->scroll) * 16;
    native_fn_0204b53c((LayoutState *)(context + 16), &point);
}
