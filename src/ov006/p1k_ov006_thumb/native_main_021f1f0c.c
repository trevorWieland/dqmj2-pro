#include "context.h"

extern u32 native_data_0221aad0[];

extern void native_fn_0201b208(void *destination, u32 fill, u32 size);

/* Allocate a zeroed block of count * size bytes through the table's allocate
   slot (+0x04). */
void *native_main_021f1f0c(u32 count, u32 size)
{
    u32 bytes = count * size;
    void *block = ((void *(*)(u32))native_data_0221aad0[1])(bytes);

    if (block != 0)
        native_fn_0201b208(block, 0, bytes);
    return block;
}
