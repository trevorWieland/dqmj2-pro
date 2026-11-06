#include "context.h"
void *native_main_0203c8a4(Allocator12 *allocator,u32 bytes)
{
    void *result=0;
    u32 used;
    if(!allocator)allocator=&native_data_020f5bf4;
    bytes=(bytes+3)&~3U;
    used=allocator->used+bytes;
    if(used<allocator->limit) {result=allocator->base+allocator->used;allocator->used=used;}
    return result;
}
