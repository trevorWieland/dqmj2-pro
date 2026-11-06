#include "context.h"
u32 *native_main_02040998(u32 key,Slot10 *table,int count)
{
    int i;
    u32 *result=0;
    i=0;
    if(count>0)do {
        if(table[i].key==0) {
            result=&table[i].data;
            native_fn_02008c14(0,result,4);
            table[i].key=key;
            break;
        }
        i++;
    } while(i<count);
    return result;
}
