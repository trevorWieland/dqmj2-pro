#include "context.h"

extern u8 native_data_0221c140[];

/* Clear the slot record's +0x1e flag. */
void native_main_021fe6d8(void)
{
    u8 *record = *(u8 **)native_data_0221c140;

    record[0x1e] = 0;
}
