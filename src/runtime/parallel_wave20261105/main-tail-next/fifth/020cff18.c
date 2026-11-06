#include "context.h"
void native_main_020cff18(void)
{
    s32 pages = (native_fn_020629e0() + 11) / 12;
    if (pages != 1 && native_fn_020d0a14() > 0) {
        native_data_021d6b48.previousC->flags7C |= 2;
        native_fn_02048a44((u8 *)native_data_021d6b48.previousC + 8, 1);
    } else native_data_021d6b48.previousC->flags7C &= ~2u;
    if (pages != 1 && native_fn_020d0a14() < pages - 1) {
        native_data_021d6b48.next10->flags7C |= 2;
        native_fn_02048a44((u8 *)native_data_021d6b48.next10 + 8, 1);
    } else native_data_021d6b48.next10->flags7C &= ~2u;
}
