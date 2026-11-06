#include "context.h"
s32 native_main_0209075c(const char *text,Address *destination)
{
    u32 h=native_fn_0209009c(text);
    if(h==0)return 0;
    destination->addr=((h>>24)&0x000000ff)|((h>>8)&0x0000ff00)|((h<<8)&0x00ff0000)|((h<<24)&0xff000000);
    return 1;
}
