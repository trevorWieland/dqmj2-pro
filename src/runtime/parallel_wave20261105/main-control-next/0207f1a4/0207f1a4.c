#include "context000.h"

State *native_main_0207f1a4(void){
    int count=native_data_021c6c14.count;
    if(count>0){do{native_fn_0207f1ec(native_data_021c6c58[count-1]);}while((count=native_data_021c6c14.count)>0);}
    native_data_021c6c14.pending=1;
    return &native_data_021c6c14;
}
