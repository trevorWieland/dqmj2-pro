#include "context.h"
s32 native_main_0202841c(CameraView *camera, s32 angle)
{
    Vec3 up;
    Mtx33 matrix;
    s32 previous;
    if (!camera) camera = native_data_020edd0c.current;
    previous = camera->angle18;
    camera->angle18 = angle;
    up.x = 0;
    up.y = 4096;
    up.z = 0;
    native_fn_02000ce8(&matrix);
    native_fn_020280a0(&matrix, angle);
    native_fn_0200103c(&up, &matrix, &camera->up);
    return previous;
}
