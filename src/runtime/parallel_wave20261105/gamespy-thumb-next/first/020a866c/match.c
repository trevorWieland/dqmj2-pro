#include "context.h"
void native_main_020a866c(DArray array, const void *newElem, int n)
{
    assert( (n >= 0) && (n <= array->count));

    if (array->count == array->capacity)
        native_fn_020a85a8(array);
    array->count++;
    if (n < array->count - 1) 
        native_fn_0201b1bc(native_fn_020a8644(array, n+1), native_fn_020a8644(array,n), 
                (array->count - 1 - n) * array->elemsize);
    native_fn_020a85c4(array, newElem, n);
}
