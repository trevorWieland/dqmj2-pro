#include "context.h"
void native_main_0209aa64 (DWCAllocType name, void * ptr, u32 size)
{
#pragma unused(size)
    SDK_ASSERTMSG(s_free, "DWC_MEMFUNC: Free function isn't defined.\n");
    if (ptr == NULL) {
        return;
    }
    ptr = native_fn_0209aa0c(ptr);
    s_free(name, ptr, ((DWCiAllocHeader *)ptr)->size + sizeof(DWCiAllocHeader));
}
