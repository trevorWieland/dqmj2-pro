#include "context.h"
void * native_main_020a87fc(DArray array, ArrayMapFn2 fn, void *clientData)
{
    int i;
    void * pcurr;

    assert(fn);

    for (i = (array->count - 1) ; i >= 0 ; i--)
    {
        pcurr = native_fn_020a8644(array,i);
        if(!fn(pcurr, clientData))
            return pcurr;
    }

    return NULL;
}
