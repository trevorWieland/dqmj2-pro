#include "context.h"
u32 native_main_02090cac(u8 *text,s32 tag)
{
    u32 year=text[0]*10+text[1]-528;
    text+=2;
    if(tag==23){
        if(year<50)year+=2000;
        else year+=1900;
    }else {
        year=year*100+(text[0]*10+text[1]-528);
        text+=2;
    }
    return (year<<16)+((text[0]*10+text[1]-528)<<8)+(text[2]*10+text[3]-528);
}
