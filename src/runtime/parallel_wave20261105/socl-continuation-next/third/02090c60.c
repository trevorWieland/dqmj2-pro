#include "context.h"
void native_main_02090c60(s8 *destination,s8 *source,s32 length)
{
    s8 *start=destination;
    if(*destination){
        while(*++destination);
        if(destination-start>=255)return;
        *destination++=',';
        *destination++=' ';
    }
    while(length-- && destination-start<255)*destination++=*source++;
    *destination=0;
}
