#include "context.h"

extern void native_fn_02203c20(u32 *arguments);

/* Publish the four-word argument block. */
void native_main_02204254(u32 first, u32 second, u32 third, u32 fourth)
{
    native_fn_02203c20(&first);
}
