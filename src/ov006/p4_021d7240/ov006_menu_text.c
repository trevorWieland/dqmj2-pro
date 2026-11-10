/*
 * ov006 packet p4-1: menu text setters and the sprite-slot builders that the
 * menu system drives. Each function is the byte-exact reconstruction of the
 * overlay at the address in its name; offsets come from the measured image.
 */
#include "context.h"

/* 0x021d79e4: set one text-list entry and clear its trailing argument. */
void native_ov006_021d79e4(u32 index, u32 a, u32 b, u32 c) {
    native_fn_ov006_021d79f8(index, a, b, c, 0);
}

/* 0x021d7ae0: redraw slot `index` with an already formatted string. */
void native_ov006_021d7ae0(u32 index, u32 a, u32 b) {
    native_fn_02049ffc(*(u8 **)(native_data_ov006_0220eb04 + index * 4));
    native_fn_02087a48(((u8 **)native_data_ov006_0220eb04)[index], 0, b, 0,
                       *(u32 *)(native_data_ov006_0220c8a0 + 4), (u8 *)a);
    native_fn_ov006_021d79d4(1);
}

/* 0x021d7d28: build `count` sprites from packed 4-byte records.
 *
 * Each record is (type, x, y, style). The style nibbles accumulate a scale in
 * var_r8 so successive rows are spaced by style.x * style.y. */
u32 native_ov006_021d7d28(void *records, s32 count) {
    u8 low;
    u8 high;
    void *sprite;
    u8 index;
    s32 scale;
    void *cursor;

    cursor = records;
    scale = 1;
    native_fn_02008c58(0, native_data_ov006_0220eb04, 0xA0);
    index = 0;
    if (count > 0) {
        do {
            ((u8 **)native_data_ov006_0220eb04)[index] =
                (u8 *)native_fn_02084924(6, ((u8 *)cursor)[0], ((u8 *)cursor)[1],
                                         ((u8 *)cursor)[2], (s32)((u8 *)cursor)[3],
                                         3, 3, scale, 1, 1);
            native_fn_02049ffc();
            sprite = ((u8 **)native_data_ov006_0220eb04)[index];
            *(u32 *)((u8 *)sprite + 0x18) |= 2;
            index++;
            low = ((u8 *)cursor)[2];
            high = ((u8 *)cursor)[3];
            cursor = (u8 *)cursor + 4;
            scale += low * high;
        } while ((s32)index < count);
    }
    *(s32 *)(native_data_ov006_0220e9a0 + 0x24) = count;
    return (u32)native_data_ov006_0220e9a0;
}

/* 0x021d8154: drain the pending glyph count, emitting every queued glyph at
 * x = 0, then reset the queue. */
void native_ov006_021d8154(void) {
    s8 index = 0;
    if (native_data_ov006_0220e9a0[0] > index) {
        u8 *source = native_data_ov006_0220e9d0;
        do {
            native_fn_0204861c(0, *source++);
            index++;
        } while (native_data_ov006_0220e9a0[0] > index);
    }
    native_data_ov006_0220e9a0[0] = 0;
}
