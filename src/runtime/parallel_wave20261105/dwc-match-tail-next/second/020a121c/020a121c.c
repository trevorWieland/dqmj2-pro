#include "context.h"
void native_main_020a121c (int profileID, const u32 data[])
{
    u32 len;
    len = data[0] + 2;
    if (len > 2) {
        native_fn_02008c28(&data[1], &native_fn_020a3d70()->svDataBak[2], sizeof(u32) * (len - 2));
    }
    native_fn_020a3d70()->svDataBak[0] = len - 1;
    native_fn_020a3d70()->svDataBak[1] = (u32)profileID;
}
