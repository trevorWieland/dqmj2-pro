#include "context.h"

/* Index a table with the caller's index (stride four per 16-bit field). */
u32 native_ov006_021f5418(u32 *record, u32 index)
{
    u32 base = record[1];

    return base + *(u32 *)(record[0] + ((index << 16) >> 14));
}
