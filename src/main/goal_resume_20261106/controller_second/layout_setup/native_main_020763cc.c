#include "layout_setup.h"

void native_main_020763cc(void)
{
    Display *display = native_fn_ov000_02215698();
    Point point;
    native_fn_ov000_022159b8(native_data_020de3f8, 4);
    point.x = 0;
    point.y = 0;
    native_fn_0204b4f4(&display->layout, &point, 224, 2, 2, 36);
    native_fn_0204b61c(&display->layout, 0);
}
