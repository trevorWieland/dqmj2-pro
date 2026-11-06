#include "context.h"
void native_main_020a8594(DArray array, int n)
{
    if (array->elemfreefn != NULL)
        array->elemfreefn(native_fn_020a8644(array,n));
}
