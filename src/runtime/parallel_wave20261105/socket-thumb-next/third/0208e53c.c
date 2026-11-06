#include "context.h"
s32 native_main_0208e53c(u32 *output,s32 mode)
{
    s32 retry;
    u32 result;
    u32 timer;
    native_fn_0208d7c0();
    native_fn_0208d764();
    if(mode==1)native_fn_0208d780(68,67,native_data_021cfcf8.server20);
    else native_fn_0208d780(68,67,0xffffffff);
    retry=0;
    do{
        result=native_fn_0208e2e0(native_fn_0208e250(mode),retry);
        if(result)break;
        ++retry;
    }while(retry<4);
    native_fn_0208d7e0();
    if(result==2){
        *output=native_data_021cfcf8.lease4C>>1;
        native_data_021cfcf8.timer38=(native_data_021cfcf8.lease4C*3)>>3;
        return 1;
    }
    timer=native_data_021cfcf8.timer38>>1;
    native_data_021cfcf8.timer38=timer;
    *output=timer;
    switch(mode){
    case 1:
        if(timer<60){*output=1;native_data_021cfcf8.timer38=native_data_021cfcf8.lease4C>>3;}
        break;
    case 2:
        if(timer<60)*output=1;
        break;
    }
    return 0;
}
