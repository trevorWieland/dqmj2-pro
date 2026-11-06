#include "context.h"
int native_main_020409f4(u32 key,Slot10 *table,int count)
{
    int result=0;
    int i=0;
    if(count>0)do {
        if(table[i].key==key) {
            native_fn_02008c14(0,&table[i].data,4);
            table[i].key=0;
            result=1;
            break;
        }
        i++;
    } while(i<count);
    return result;
}
