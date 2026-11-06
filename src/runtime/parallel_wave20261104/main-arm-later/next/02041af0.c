#include "context.h"
GlobalSlot10 *native_main_02041af0(u32 key)
{
    int i;
    GlobalSlot10 *result=0;
    i=0;
    do {
        if(native_data_020f65b4[i].key==key) {result=&native_data_020f65b4[i];break;}
        i++;
    } while(i<64);
    return result;
}
