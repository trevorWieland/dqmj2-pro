#include "context000.h"

int native_main_0207d8e4(int mode,int value){
    const Observed *context=native_fn_0207d2c8(mode);
    if(mode==0)return value;
    if(context->code==5)value=value*6/5;
    return value;
}
