#include "child_score.h"
s32 native_ov001_022263d8(s32 *available, const void *roster) {
    s32 values[3];
    s32 scores[3];
    s32 index, result;
    s32 best = 99;
    const ChildScoreRecord *object = roster;
    native_fn_02008e0c(available, values, sizeof(values));
    index = 0;
    do {
        if (values[index]) {
            scores[index] = object->child->valuecc;
            if (scores[index] != 0 && best > scores[index]) best = scores[index];
        }
        index++;
        object++;
    } while (index < 3);
    index = 0;
    do {
        if (values[index] && best != scores[index]) values[index] = 0;
        index++;
    } while (index < 3);
    result = ov001_count_candidates_02223f20(values);
    if (result > 0) native_fn_02008e0c(values, available, sizeof(values));
    return result;
}
