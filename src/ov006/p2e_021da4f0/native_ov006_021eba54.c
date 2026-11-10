#include "context.h"

/* Dispatch the table entry the scene block selects, once the block reports its
   dispatch state. */
void native_ov006_021eba54(void)
{
    if (native_data_ov006_02219290.field_14 != 1)
        return;
    (*(void (**)(void))((u8 *)native_data_ov006_022087e4
                        + native_data_ov006_02219290.field_1c * 0xc))();
}
