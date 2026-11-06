#include "context.h"
s32 native_main_0208e820(const u8 *text,u32 *output)
{
    u32 address=0;
    s32 part=0;
    const u8 *end;
    do{
        u32 value;
        address<<=8;
        value=native_fn_0208e7f8(text,&end);
        if(text==end)return 0;
        text=end;
        if(value>255 || (part!=3 && *text++!=46) || (part==3 && *text!=0))return 0;
        address|=value;
        ++part;
    }while(part<4);
    *output=address;
    return 1;
}
