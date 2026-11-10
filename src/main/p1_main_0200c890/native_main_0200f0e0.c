#include "context.h"

extern u32 native_fn_0200e800(u32 command, u32 arg1, u32 arg2);

/* Tail-call command 0x12 with the low half of the argument. */
u32 native_main_0200f0e0(u32 value)
{
    return native_fn_0200e800(0x12, (u16)value, 0);
}
