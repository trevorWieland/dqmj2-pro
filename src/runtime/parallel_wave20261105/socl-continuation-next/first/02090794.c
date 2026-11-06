#include "context.h"
const char *native_main_02090794(s32 family,const void *source,char *destination,u32 length)
{
    u32 word;
    u8 bytes[4];
    if(family!=2)return 0;
    if(length<16)return 0;
    native_fn_02008e0c(source,&word,sizeof(word));
    native_fn_020907e4(word,bytes);
    native_fn_020061ac(destination,16,native_data_020de81c,bytes[3],bytes[2],bytes[1],bytes[0]);
    return destination;
}
