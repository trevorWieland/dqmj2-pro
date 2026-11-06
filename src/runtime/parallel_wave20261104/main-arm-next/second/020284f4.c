#include "context.h"
void native_main_020284f4(CameraView *camera, s32 angle)
{
    Vec3 difference;
    Vec3 transformed;
    Mtx33 matrix;
    if (!camera) camera = native_data_020edd0c.current;
    difference.x = (s32)((u32)camera->position.x - (u32)camera->target.x);
    difference.y = (s32)((u32)camera->position.y - (u32)camera->target.y);
    difference.z = (s32)((u32)camera->position.z - (u32)camera->target.z);
    native_fn_02000ce8(&matrix);
    native_fn_02028044(&matrix, angle);
    native_fn_0200103c(&difference, &matrix, &transformed);
    camera->position.x = (s32)((u32)camera->target.x + (u32)transformed.x);
    camera->position.y = (s32)((u32)camera->target.y + (u32)transformed.y);
    camera->position.z = (s32)((u32)camera->target.z + (u32)transformed.z);
}
