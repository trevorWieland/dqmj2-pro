#include "context000.h"

unsigned int native_main_0207d198(const u8 *input,unsigned int context,unsigned int value){
    int i;
    for(i=0;i<64 && input[i]!=0;++i){if(input[i]==16)value=native_fn_0207d1e4(context,value);}
    return value;
}
