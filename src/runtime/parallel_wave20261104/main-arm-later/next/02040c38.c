#include "context.h"
int native_main_02040c38(const signed char *first,const signed char *second)
{
    int result;
    for(;;) {
        signed char a=*first;
        signed char b=*second;
        if((u8)(a-'A')<=25)a+=32;
        if((u8)(b-'A')<=25)b+=32;
        result=a-b;
        if(result)break;
        if(a==0)break;
        first++;second++;
    }
    return result;
}
