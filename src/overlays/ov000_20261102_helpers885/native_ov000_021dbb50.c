#include "context.h"
u32 native_ov000_021dbb50(s32 index, u32 tree, u32 indicesWord, u32 unusedWord3, u32 triangles, u32 point, s32 limit)
{
    s16 *indices;
    s32 processed;
    s32 count;
    indices = (s16 *) indicesWord;
    indices[0] = (s16) index;
    processed = 0;
    count = 1;
    do {
        count = native_fn_ov000_021db968(indices[processed], tree, indicesWord, count, triangles, point, limit);
        processed++;
    } while (processed < count && processed < limit);
    return (u32) processed;
}
