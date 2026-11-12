#include "child_score.h"
s32 native_ov001_02226290(s32 *available, const void *roster) {
    s32 values[3];
    s32 index, result;
    const ChildScoreRecord *object = roster;
    native_fn_02008e0c(available, values, sizeof(values));
    index = 0;
    do {
        if (values[index] && object->child->flagb1 != 0) values[index] = 0;
        object++;
        index++;
    } while (index < 3);
    result = ov001_count_candidates_02223f20(values);
    if (result > 0) native_fn_02008e0c(values, available, sizeof(values));
    return result;
}
