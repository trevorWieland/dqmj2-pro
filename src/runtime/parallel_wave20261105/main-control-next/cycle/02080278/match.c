#include "context.h"
int native_main_02080278(u8 *value){
    Match match;
    if(native_fn_0207ffb4(value,&match)==0)return 0;
    do{++match.column;match.column&=3;}while(native_data_020db298[match.row][match.column][0]==0);
    native_fn_02008e0c(native_data_020db298[match.row][match.column],value,3);
    return 1;
}
