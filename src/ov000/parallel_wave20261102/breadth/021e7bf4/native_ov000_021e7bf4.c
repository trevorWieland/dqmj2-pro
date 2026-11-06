#include "context.h"
s32 native_ov000_021e7bf4(void)
{
    s32 result = -1;
    s32 index;
    for (index = 0;
    index < 8;
    index++)
{
    if (data_ov000_0223526c[index].flag == 0)
{
    result = index;
    break;
   
}
} return result;
   
}
