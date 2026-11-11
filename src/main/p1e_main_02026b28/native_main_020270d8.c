#include "context.h"

extern u16 native_data_027fffa8;

extern u32 native_fn_020ba564(void);
extern u32 native_fn_02084718(void);
extern u32 native_fn_020befa8(void);
extern u32 native_fn_02027f30(u32 value);
extern void native_fn_02064594(void);
extern void native_fn_0200e964(u32 value, u32 arg);
extern void native_fn_0200eb80(u32 command, u32 arg1, u32 arg2);

/* Boot-state step for the first frames: drive the pending sound/task command
   once the early subsystem handshake has completed.  Returns 0 while waiting,
   1 once the step consumed a command. */
u32 native_main_020270d8(void)
{
    u32 flag;

    if (native_fn_020ba564() != 0 || native_fn_02084718() == 1) {
        flag = (native_data_027fffa8 & 0x8000) >> 15;
        if (flag != 1)
            native_fn_02064594();
        else
            native_fn_0200e964(2, 0);
        return 0;
    }
    if (native_fn_020befa8() != 0)
        return 0;
    flag = (native_data_027fffa8 & 0x8000) >> 15;
    if (flag == 0) {
        native_fn_02064594();
        return 0;
    }
    if (native_fn_02027f30(0) == 0)
        return 0;
    native_fn_0200eb80(0xc, 0, 0);
    native_fn_02064594();
    return 1;
}

