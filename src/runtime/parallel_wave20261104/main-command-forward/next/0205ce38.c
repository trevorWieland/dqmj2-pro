#include "context.h"
int native_main_0205ce38(u32 index,int amount)
{
    int result=0;
    if(index<32) {
        Record11c *record=&native_data_021043ac[index];
        if(record->field0==3) {
            int value=(int)(((s64)amount*410LL+0x800LL)>>12);
            record->field90.words[0]=value;
            record->field90.words[1]=value;
            record->field90.words[2]=value;
            result=1;
        }
    }
    return result;
}
