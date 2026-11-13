#include "context.h"

/* native_ov001_022294c8.c: 52 bytes at 0x022294c8 in ov001.
 * s32 func(void): copy the 12-byte 0x0222e5c0 block to the stack, publish it
 * through 0x02224050 and query the result with 0x02226cb0. */
typedef struct {
    s32 a;
    s32 b;
    s32 c;
} Block;

s32 native_ov001_022294c8(void)
{
    Block local = *(Block *)native_data_ov001_0222e5c0;

    ov001_pick_random_candidate_02224050(&local);
    return ov001_first_candidate_02226cb0(&local);
}
