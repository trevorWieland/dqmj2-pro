#include "context.h"

extern u8 native_data_0221a92c[];

/* Call the single entry stored at 0x0221a92c. */
void native_main_021ebb2c(u32 argument)
{
    ((void (*)(u32)) * (u32 *)native_data_0221a92c)(argument);
}


