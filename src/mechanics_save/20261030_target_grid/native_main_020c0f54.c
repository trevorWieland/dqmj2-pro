#include "target_grid_types_20261030.h"
s32 native_main_020c0f54(s32 x, s32 y) {
    u8 originX;
    u8 originY;
    native_fn_0206c1d4(native_fn_02069000(), &originX, &originY);
    originX = (originX + 1) * 8;
    originY = (originY + 1) * 8;
    if (x >= originX && x < originX + 80 && y >= originY && y < originY + 120) {
        return ((x - originX) / 40) * 3 + (y - originY) / 40;
    }
    return -1;
}
