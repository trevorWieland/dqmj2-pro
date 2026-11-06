#include "context.h"
void native_ov003_021dfda8(u32 flag) {
    native_data_ov003_021e041c[0] = flag;
    if (flag != 0) {
        native_data_ov003_021e0d18.object->flags |= 2;
    } else {
        native_data_ov003_021e0d18.object->flags &= ~2U;
    }
    native_data_02101ae8.dirty = 1;
}
