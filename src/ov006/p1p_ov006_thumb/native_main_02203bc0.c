#include "context.h"

extern u8 native_data_0221c188[];
extern void native_fn_0202b328(u32 handle);

/* Release the active handle and clear the pointer word. */
void native_main_02203bc0(void)
{
    native_fn_0202b328(*(u32 *)native_data_0221c188);
    *(u32 *)native_data_0221c188 = 0;
}
