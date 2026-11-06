#include "context000.h"

int native_main_0207d31c(int mode,int value,unsigned int index){
    if(native_fn_0207b058(index,2)){
        switch(mode){
        case 1:value=value*21/20;break;
        case 2:value=value*11/10;break;
        case 3:value=value*23/20;break;
        case 4:value=value*6/5;break;
        }
    }
    return value;
}
