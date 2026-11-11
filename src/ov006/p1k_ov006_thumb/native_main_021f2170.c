#include "context.h"

extern u32 native_data_0221aad0[];
extern void native_fn_021f2124(u8 *buffer);

/* Build one 0x0c-byte request and submit it through the +0x7c entry. */
void native_main_021f2170(void)
{
    u8 buffer[0x0c];

    native_fn_021f2124(buffer);
    ((void (*)(u8 *))native_data_0221aad0[0x1f])(buffer);
}
