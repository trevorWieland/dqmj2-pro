#include "context.h"
u32 native_main_02071b28(void)
{
    native_fn_02061944();
    s32 selected=(s32)((u32)native_data_021c50e8.flags.raw<<31)>>31;
    if(selected!=0)native_fn_02072030();
    native_fn_020622ec(6,11,0);
    s8 i=0;
    u32 result;
    do {
        u32 amount=native_fn_02065d28(native_data_020daf42[i*2]);
        result=native_data_021c50e8.counter-amount;
        i+=1;
        native_data_021c50e8.counter=result;
    } while(i<9);
    return result;
}
