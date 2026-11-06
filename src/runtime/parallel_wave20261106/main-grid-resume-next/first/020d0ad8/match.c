#include "context.h"
void native_main_020d0ad8(u32 first, u32 second)
{
    s32 i, j;
    u32 id;
    s32 nfirst, nsecond;
    s32 x, y;
    nfirst = (s32)native_fn_02062aa0();
    nsecond = (s32)native_fn_02062ad0();
    for (i = 0; i < 12; ++i) {
        native_fn_020cfa78(i, &x, &y);
        id = native_fn_0207cd98(native_data_main_021d6b5c.page * 12 + i);
        for (j = 0; j < nfirst; ++j) {
            if (native_fn_02062a50(j)->id == id) {
                native_fn_02065818(first, (s8)(x / 8), (s8)(y / 8));
                break;
            }
        }
        for (j = 0; j < nsecond; ++j) {
            if (native_fn_02062a88(j)->id == id) {
                native_fn_02065818(second, (s8)(x / 8), (s8)(y / 8));
                break;
            }
        }
    }
}
