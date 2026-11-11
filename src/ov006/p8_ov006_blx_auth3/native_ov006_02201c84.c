#include "context.h"

/* 0x0221C164 is the ov006 mode descriptor shared with other mode rows: word 0
   is the mode-change callback (may be null) and word 1 a pointer to the mode
   state. The state's mode word is at +0x40; the 0x13E0 and 0x1C00 offsets are
   the argument block and the result block of the ARM evaluator. */
struct native_mode_0221c164 {
    u32 callback;
    u8 *state;
};

extern struct native_mode_0221c164 native_data_ov006_0221c164;
extern u8 native_data_ov006_0220e804[];
extern u8 native_data_ov006_0220e834[];

extern s32 native_fn_020136fc(u32 first, u32 second, u32 third);
extern void native_ov006_022012c0(s32 result);

/* ov006 row 0x02201C84: 112 bytes. Run the mode evaluator over the +0x13E0
   argument block and classify its answer: 7 hands the 0x0220E804 table to the
   mode callback and succeeds, 5 hands 0x0220E834 and reports the answer to the
   mode dispatcher, any other non-zero answer is only reported, and zero is the
   only result that returns 1. The call at +0x12 targets ARM code and is a BLX
   immediate in the image; the two callback calls are indirect. Unknown: what
   the evaluator reads and why answers 5 and 7 take different tables. */
s32 native_ov006_02201c84(u32 argument)
{
    s32 result = native_fn_020136fc(native_data_ov006_0221c164.state + 0x13E0, argument,
                                    (u32)(native_data_ov006_0221c164.state + 0x1C00));

    if (result == 7) {
        if (native_data_ov006_0221c164.callback != 0)
            ((void (*)(u32, u32))native_data_ov006_0221c164.callback)(
                0x08000000, (u32)native_data_ov006_0220e804);
        return 0;
    }
    if (result == 5) {
        if (native_data_ov006_0221c164.callback != 0)
            ((void (*)(u32, u32))native_data_ov006_0221c164.callback)(
                0x08000000, (u32)native_data_ov006_0220e834);
        native_ov006_022012c0(result);
        return 0;
    }
    if (result != 0) {
        native_ov006_022012c0(result);
        return 0;
    }
    return 1;
}
