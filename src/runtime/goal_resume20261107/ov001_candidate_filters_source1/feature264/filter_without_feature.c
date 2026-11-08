#include "feature_record.h"

s32 native_ov001_02225854(s32 *available, void *roster) {
    s32 values[3];
    s32 index, result;
    FeatureRecordView *object = roster;
    native_fn_02008e0c(available, values, sizeof(values));
    index = 0;
    do {
        if (values[index]) {
            if (native_fn_ov001_02210ba8(object) != 0) {
                values[index] = 0;
            }
        }
        index++;
        object++;
    } while (index < 3);
    result = native_fn_ov001_02223f20(values);
    if (result > 0) {
        native_fn_02008e0c(values, available, sizeof(values));
    }
    return result;
}
