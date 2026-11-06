#include "context.h"
void native_main_020a85a8(DArray array)
{
    array->capacity +=  array->growby;
    array->list = native_fn_020a928c(array->list, array->capacity * array->elemsize);
    assert(array->list);
}
