#include "context.h"
void native_main_020a86ec(DArray array, int n)
{
       assert( (n >= 0) && (n < array->count));

    if (n < array->count - 1) 
        native_fn_0201b1bc(native_fn_020a8644(array,n),native_fn_020a8644(array,n+1),
                (array->count - 1 - n) * array->elemsize);
    array->count--;
}
