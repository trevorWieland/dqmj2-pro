#include "context.h"

extern u8 native_data_0221a920[];

/* Call the single entry stored at 0x0221a920. */
void native_main_021ebb1c(u32 argument)
{
    ((void (*)(u32)) * (u32 *)native_data_0221a920)(argument);
}


