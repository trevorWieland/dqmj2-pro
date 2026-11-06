#include "context.h"
u16 native_main_0208a508(u16 channel)
{
    s32 i;
    for (i = 0; i < 13; i++)
    {
        if (native_data_021cfcb4->option & (0x0001 << (((channel + i) % 13) + 1)))
        {
            break;
        }
    }
    return(u16) (((channel + i) % 13) + 1);
}
