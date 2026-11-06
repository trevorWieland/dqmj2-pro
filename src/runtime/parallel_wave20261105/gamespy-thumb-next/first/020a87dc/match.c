#include "context.h"
void native_main_020a87dc(DArray array, ArrayMapFn fn, void *clientData)
{
    int i;

    assert(fn);

    for (i = (array->count - 1) ; i >= 0 ; i--)
        fn(native_fn_020a8644(array,i), clientData);
        
}
