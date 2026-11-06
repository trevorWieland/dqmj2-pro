#include "context.h"
int native_main_0208fb2c(int length){
SocView *soc=native_data_020e33e4.current4->specificA4;
int temp=0;
u32 enabled=native_fn_02007ff4();
if(soc){if(soc->mss2E>0 && soc->window2C>0){temp=2*minimum(minimum(soc->mss2E,soc->window2C),(int)native_data_021d1550.mss24);}else{temp=2*(int)native_data_021d1550.mss24;}}
else{temp=2*(int)native_data_021d1550.mss24;}
(void)native_fn_02008008(enabled);
if(temp>0){int count=native_fn_02026144(length,temp);if(count>0){return temp*count;}}
return length;
}
