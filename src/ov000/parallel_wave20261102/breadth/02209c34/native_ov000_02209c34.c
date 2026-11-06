#include "context.h"
s32 native_ov000_02209c34(void)
{
    s32 result = -1;
    s32 index;
    for (index = 0;
    index < 48;
    index++)
{
    if (data_ov000_02238634[index].flag == 0)
{
    result = index;
    break;
   
}
} return result;
   
}
