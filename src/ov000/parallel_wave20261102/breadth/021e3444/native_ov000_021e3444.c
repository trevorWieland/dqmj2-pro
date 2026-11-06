#include "context.h"
s32 native_ov000_021e3444(void)
{
    s32 result = -1;
    s32 index;
    for (index = 0;
    index < 64;
    index++)
{
    if (data_ov000_02234388[index].flag == 0)
{
    result = index;
    break;
   
}
} return result;
   
}
