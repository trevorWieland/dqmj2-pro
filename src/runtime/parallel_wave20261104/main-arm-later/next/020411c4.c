#include "context.h"
int native_main_020411c4(const void *key,void *destination,u32 argument)
{
    int result=0;
    void *data=native_fn_02040d18(key,argument);
    if(data)result=native_fn_020411f4(destination,data);
    return result;
}
