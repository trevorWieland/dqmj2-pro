#include "context.h"
u32 *native_main_02040a50(u32 key,Slot8 *table,int count)
{
    int i;
    u32 *result=0;
    i=0;
    if(count>0)do {
        if(table[i].key==key) {result=&table[i].data;break;}
        i++;
    } while(i<count);
    return result;
}
