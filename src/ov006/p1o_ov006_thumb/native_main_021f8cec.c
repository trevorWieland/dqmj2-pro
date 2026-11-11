#include "context.h"

extern u8 native_data_0220b5d4[];
extern u8 native_data_0221c0d8[];
extern void native_fn_021fe580(u32 record, u32 value, u32 same_value);

/* Forward the current mode byte and the list head's +8 word. */
void native_main_021f8cec(void)
{
    volatile u8 scratch;
    u8 value = native_data_0220b5d4[0];
    u32 *record = *(u32 **)(native_data_0221c0d8 + 4);

    scratch = value;
    native_fn_021fe580(record[2], value, value);
}
