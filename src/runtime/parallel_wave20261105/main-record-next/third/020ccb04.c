#include "context.h"

u32 native_main_020ccb04(u32 value) {
    native_data_020e2f38[0] = value;
    native_fn_0204b61c(*(u32*)(native_data_021d682c+0xc),value);
    *(int*)(native_data_02101ae8+0xc84) = 1;
    return (u32)native_data_02101ae8;
}
