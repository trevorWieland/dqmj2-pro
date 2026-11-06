#include "context.h"
Words3 * native_main_0205cdf0(u32 index,Words3 *destination)
{
    Words3 *result=0;
    if(index<32) {
        Record11c *record=&native_data_021043ac[index];
        if(record->field0==3) {result=&record->field84;if(destination)*destination=*result;}
    }
    return result;
}
