#include "../context.h"

/* 0x021e86cc: look up a byte pair and report whether its row is past the cursor. */
u32 native_ov001_021e86cc(u32 arg0, s32 a, s32 b) {
    s32 i = 0;
    do {
        if (((PairEntry *)native_data_ov001_02238d40)[i].a == a &&
            ((PairEntry *)native_data_ov001_02238d40)[i].b == b) {
            return i > (s32)arg0;
        }
        i++;
    } while (i < 6);
    return 0;
}
