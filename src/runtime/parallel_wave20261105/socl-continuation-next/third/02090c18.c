#include "context.h"
s32 native_main_02090c18(u8 **cursor)
{
    u8 *next=*cursor;
    s32 value=*next++;
    if(value&128){
        s32 count=value&127;
        value=0;
        while(count--){
            if(value&0xff000000)return -1;
            value=(value<<8)+*next++;
        }
    }
    *cursor=next;
    return value;
}
