#include "context.h"
s32 native_main_02091518(u8 *entries,s32 count,s32 width,u16 method)
{
    u32 value;
    s32 index;
    for(index=0;index<count;index++){
        value=(entries[0]<<8)+entries[1];
        if(width==3)value=(value<<8)+entries[2];
        if(value==method)return 1;
        entries+=width;
    }
    return 0;
}
