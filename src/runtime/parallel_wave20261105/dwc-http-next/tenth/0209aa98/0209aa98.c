#include "context.h"
void * native_main_0209aa98 (DWCAllocType name, void * ptr, u32 oldsize, u32 newsize, int align)
{
    void * newptr;
    newptr = native_fn_0209aa44(name, newsize, align);
    if (newptr == NULL) {
        return NULL;
    }
    if (ptr != NULL) {
        oldsize = native_fn_0209aa20(ptr);
        native_fn_02008e0c(ptr, newptr, (oldsize > newsize) ? newsize : oldsize);
        native_fn_0209aa64(name, ptr, oldsize);
    }
    return newptr;
}
