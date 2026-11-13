#include "compatibility_record.h"

s32 native_ov001_02226598(s32 *available, const void *reference, const void *roster) {
    s32 values[3];
    s32 index, result;
    const CompatibilityRecordView *fixed = reference;
    const CompatibilityRecordView *object = roster;
    native_fn_02008e0c(available, values, sizeof(values));
    index = 0;
    do {
        if (values[index]) {
            if (fixed->stage + object->stage > 4 || fixed->category == object->category) {
                values[index] = 0;
            }
        }
        index++;
        object++;
    } while (index < 3);
    result = ov001_count_candidates_02223f20(values);
    if (result > 0) native_fn_02008e0c(values, available, sizeof(values));
    return result;
}
