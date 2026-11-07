#include "context.h"
SlotState*native_ov000_0221f910(void)
{
    s32 i;
    u32 p1;
    SlotState*result;
    native_fn_ov000_0221c758(16,((SetupContext*)native_fn_ov000_0221c658())->field16,12,17,5,15,14,1,0);
    native_fn_ov000_0221c758(17,((SetupContext*)native_fn_ov000_0221c658())->field16,18,17,11,1,1,1,0);
    native_fn_ov000_0221c758(18,((SetupContext*)native_fn_ov000_0221c658())->field16,19,17,12,1,6,1,0);
    native_fn_ov000_0221c758(19,((SetupContext*)native_fn_ov000_0221c658())->field16,20,17,18,1,1,1,0);
    i=0;
    p1=6;
    do{
        result=native_fn_ov000_0221c758((s8)(i+20),((SetupContext*)native_fn_ov000_0221c658())->field16,1,18,p1,13,2,0,1);
        i++;
        p1+=2;
    }while(i<6);
    return result;
}
