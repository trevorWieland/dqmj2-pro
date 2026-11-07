#include "../../../../resource_path_api.h"
#include "context.h"
void native_main_0205ff4c(CleanupEntry *entry)
{
    CleanupObject *object=entry->field4;
    if(object->field2e==0)native_fn_02084f4c(object);
    else native_fn_02084f60(object);
    entry->field2=0;
    entry->field4=0;
}
