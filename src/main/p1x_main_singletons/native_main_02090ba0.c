#include "context.h"

extern u32 native_data_020e33e4[];
extern void native_fn_02006acc(u32 word, u32 value);

/* Forward small indices to the ARM routine 0x02006acc. */
void native_main_02090ba0(u32 value)
{
    if (value < 0x20)
        native_fn_02006acc(native_data_020e33e4[1], value);
}
