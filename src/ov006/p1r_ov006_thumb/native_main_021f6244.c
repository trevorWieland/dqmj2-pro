#include "context.h"

extern void native_fn_021f27d4(u32 table, u32 argument);
extern u8 native_data_0220dc04[];
extern u8 native_data_02004cd8[];

/* Display family row: submit the table word, then rewrite the 3-bit field of
   the u16 registers at 0x04001008 and 0x04000008. */
void native_main_021f6244(void)
{
    volatile u16 *first;
    volatile u16 *second;

    native_fn_021f27d4((u32)native_data_0220dc04, (u32)native_data_02004cd8);
    first = (volatile u16 *)0x04001008;
    second = (volatile u16 *)0x04000008;
    first[0] = (u16)((first[0] & ~3) | 3);
    first[1] = (u16)((first[1] & ~3) | 3);
    second[0] = (u16)((second[0] & ~3) | 3);
    second[1] = (u16)((second[1] & ~3) | 3);
    second[2] = (u16)((second[2] & ~3) | 3);
}
