#include "context.h"
void native_main_0207313c(void)
{
    s32 index=native_data_021c6124.index;
    native_data_021c5a24.status=0;
    u32 low=native_data_021c5a24.flags.low;
    if(low==0){
        u8 kind=native_fn_02065d88(index)->kind;
        switch(kind){
        case 1:case 2:break;
        case 26:native_data_021c5a24.status=15;break;
        }
    }
    native_fn_ov000_021e7b9c(84);
    native_fn_020756e4(-1,-1,4);
}
