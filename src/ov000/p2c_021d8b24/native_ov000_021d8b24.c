#include "context.h"

/* Build the position vector for the three axis values: start from the unit
   z vector, rotate it by each axis value in turn, offset it, and hand it to the
   renderer. */
void native_ov000_021d8b24(s32 *offset, s32 *angles)
{
    Vec3 start;
    Vec3 after_x;
    Vec3 after_y;
    Vec3 position;
    u8 matrix[36];

    start.x = 0;
    start.y = 0;
    start.z = 0x1000;
    native_fn_02000ce8(matrix);
    native_fn_02027fe8(matrix, native_fn_02028158(angles[0]));
    native_fn_0200103c(&start, matrix, &after_x);
    native_fn_02000ce8(matrix);
    native_fn_02028044(matrix, native_fn_02028158(angles[1]));
    native_fn_0200103c(&after_x, matrix, &after_y);
    native_fn_02000ce8(matrix);
    native_fn_020280a0(matrix, native_fn_02028158(angles[2]));
    native_fn_0200103c(&after_y, matrix, &position);
    position.x += offset[0];
    position.y += offset[1];
    position.z += offset[2];
    native_fn_ov000_021d8eb4(&position, offset, 0, 1);
}
