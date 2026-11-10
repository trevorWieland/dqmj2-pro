/*
 * ov006 packet p4-1: label refresh for one character record.
 *
 * The record header at 0x021d9ed8 is 0x7a bytes of name text followed by the
 * four measured bounding boxes; each helper writes one bounds halfword.
 */
#include "context.h"

/* 0x021d9ed8: refresh the label and bounding boxes of an active record. */
s32 native_ov006_021d9ed8(u8 *context) {
    u8 buffer[64];
    u32 active = *(u32 *)(context + 0x14);
    s32 result;

    if (active == 0) {
        return active;
    }
    native_fn_0207b460(*(s16 *)(context + 0x18), context[0x1a], context + 0x7a, buffer);
    context[0x31] = 0;
    context[0x33] = 0;
    *(u16 *)(context + 0x24) = (u16)native_fn_0207c2b8(context + 0x20, buffer);
    *(u16 *)(context + 0x26) = (u16)native_fn_0207c3d8(context + 0x20, buffer);
    *(u16 *)(context + 0x24) = (u16)native_fn_0207c18c(context + 0x20, buffer);
    result = native_fn_0207c1b8(context + 0x20, buffer);
    *(u16 *)(context + 0x26) = (u16)result;
    return result;
}
