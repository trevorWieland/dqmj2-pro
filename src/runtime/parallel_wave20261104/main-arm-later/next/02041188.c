#include "context.h"
int native_main_02041188(void *destination,const void *key,u32 argument)
{
    int result=0;
    void *data=native_fn_0203cf20(key,argument,-1);
    if(data && native_fn_020411f4(destination,data))result=1;
    return result;
}
