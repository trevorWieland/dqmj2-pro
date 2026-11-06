#include "context.h"
void native_main_02072568(s32 index,u32 value)
{
    u32 previous=native_data_021c4f78[index];
    if(previous==value)return;
    native_data_021c4f78[index]=value;
    native_fn_0206de44(1);
}
