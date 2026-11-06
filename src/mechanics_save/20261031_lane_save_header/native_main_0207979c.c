#include "save_operations_types_20261030.h"
u32 native_main_0207979c(void) {
    SaveHeaderSummary *summary = &native_data_021c65d0;
    u8 valid = native_fn_0207df2c(0,native_data_021c65a8);
    int second;
    native_data_021c6544.headerValid = valid;
    if (valid) {
        int count = summary->rawCount;
        native_data_021c6544.first = (3-count)*2+11;
        second = (count+3)*2;
        native_data_021c6544.second = second;
    } else {
        native_data_021c6544.first = 17;
        second = 6;
        native_data_021c6544.second = second;
    }
    return second;
}
