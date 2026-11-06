#include "context.h"
u32 native_ov000_021dbbb8(u32 contextWord, u32 point)
{
    u8 *context;
    u8 *mesh;
    s32 index;
    u32 count;
    u32 field_000c;
    s32 field_0010;
    u32 field_019c;
    u32 field_0198;
    context = (u8 *) contextWord;
    mesh = (u8 *) data_ov000_0223142c.mesh;
    index = (s16) *(u32 *) (context + 8);
    field_000c = *(u32 *) (mesh + 0xC);
    field_019c = *(u32 *) (mesh + 0x19C);
    field_0198 = *(u32 *) (mesh + 0x198);
    field_0010 = *(s8 *) (context + 0x10);
    *(s16 *) (context + 0x12) = (s16) index;
    count = native_fn_ov000_021dbb50(index, (u32) mesh + field_0198, contextWord + 0x12, field_019c, (u32) mesh + field_000c, point, field_0010);
    context[0x11] = (u8) count;
    return count;
}
