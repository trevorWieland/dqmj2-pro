#include "context.h"
void * native_main_0209aa44 (DWCAllocType name, u32 size, int align)
{
    void * ptr;
    SDK_ASSERTMSG(s_alloc, "DWC_MEMFUNC: Allocator function isn't defined.\n");
    SDK_ASSERTMSG((align <= 32) && (align >= -32), "DWC_Alloc() dosen't support to align over 32 bytes order");
    ptr = s_alloc(name, size + sizeof(DWCiAllocHeader), align);
    if (ptr == NULL)
        return NULL;
    return native_fn_0209aa10(ptr, size);
}
