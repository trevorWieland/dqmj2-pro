#include "context.h"
const Record *native_main_0207d2c8(int value){
    int index=0;
    if(native_data_021c6bf4->id!=-1){
        do{
            if(value==native_data_021c6bf4[index].id)return &native_data_021c6bf4[index];
            ++index;
        }while(native_data_021c6bf4[index].id!=-1);
    }
    return 0;
}
