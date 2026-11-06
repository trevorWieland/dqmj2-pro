#include "context.h"
void native_main_020a86b8(DArray array, const void *newElem, ArrayCompareFn comparator)
{
    int n;
    void *res;
    int found;
    assert( comparator);
    res=native_fn_020a8884(newElem, array->list,	array->count, array->elemsize, comparator, &found);
    n = (((char *)res - (char *)array->list) / array->elemsize);
    native_fn_020a866c(array, newElem, n);
}
