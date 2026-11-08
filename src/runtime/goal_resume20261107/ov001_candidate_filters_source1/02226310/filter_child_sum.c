#include "child_score.h"
s32 native_ov001_02226310(s32 *available, const void *roster) {
    s32 values[3];
    s32 scores[3];
    s32 index, result;
    s32 best = 0;
    const ChildScoreRecord *object = roster;
    native_fn_02008e0c(available, values, sizeof(values));
    index = 0;
    do {
        if (values[index]) {
            scores[index] = object->child->value28 + object->child->value30;
            if (scores[index] > best) best = scores[index];
        }
        index++;
        object++;
    } while (index < 3);
    index = 0;
    do {
        if (values[index] && scores[index] < best) values[index] = 0;
        index++;
    } while (index < 3);
    result = native_fn_ov001_02223f20(values);
    if (result > 0) native_fn_02008e0c(values, available, sizeof(values));
    return result;
}
