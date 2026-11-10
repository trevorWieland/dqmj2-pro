/*
 * ov006 packet p4-1: record list layout, status labels and the hint panel.
 * All offsets are measured from the overlay image.
 */
#include "context.h"

extern u8 native_data_ov006_0220cb94[];
extern u8 native_data_ov006_0220cba0[];
extern u32 native_fn_02044cdc(u32 id);
extern u32 native_fn_02044dc4(u32 species, u32 form);
extern u8 *native_fn_02062a50(s32 index);
extern u32 native_fn_02062aa0(void);
extern void native_fn_ov006_021d7e34(void);
extern void native_fn_ov006_021d7ebc(u32 value, u32 a, u32 b);

/* 0x021da864: lay out the visible record list.
 *
 * First pass scales every entry and stores the three label columns; the
 * second pass writes the name, level and class strings for each row. */
u32 native_ov006_021da864(void) {
    u32 id;
    void *record;
    void *row;
    s32 delta;
    s32 i;
    u8 y;
    s32 rowIndex;

    native_fn_ov006_021d7860();
    native_fn_ov006_021d77f8(2);
    y = 8;
    i = 0;
    if ((s32)native_fn_02062aa0() > 0) {
        do {
            id = native_fn_02044cdc(*(s16 *)((u8 *)native_fn_02062a50(i) + 0x18));
            delta = y + (s8)native_data_ov006_0220cb94[id];
            row = native_data_ov006_0220cba0 + i * 4;
            *(u8 *)((u8 *)row + 0x21) = (u8)delta;
            *(u8 *)((u8 *)row + 0x15) = (u8)delta;
            i++;
            *(u8 *)((u8 *)row + 0x2D) = (u8)(delta + 2);
            y = (u8)(y + (id + 1) * 5);
        } while (i < (s32)native_fn_02062aa0());
    }
    native_fn_ov006_021d7d28(native_data_ov006_0220cba0, 0xE);
    native_fn_ov006_021d79e4(0, 15, 2, 0x81);
    native_fn_ov006_021d79e4(3, 15, 2, 0x84);
    rowIndex = 0;
    if ((s32)native_fn_02062aa0() > 0) {
        do {
            record = native_fn_02062a50(rowIndex);
            native_fn_ov006_021d7b3c((u8)(rowIndex + 8), (u32)record,
                                     *(s16 *)((u8 *)record + 0x18));
            native_fn_ov006_021d79e4((u8)(rowIndex + 0xB), 15, 2,
                                     (u16)(*(u8 *)((u8 *)record + 0x32) + 0x2C));
            native_fn_ov006_021d79e4((u8)(rowIndex + 5), 15, 2,
                                     (u16)(native_fn_02044dc4(*(s16 *)((u8 *)record + 0x18),
                                                              *(u8 *)((u8 *)record + 0x1A)) + 0x5F));
            rowIndex++;
        } while (rowIndex < (s32)native_fn_02062aa0());
    }
    native_fn_ov006_021daaf0();
    native_fn_ov006_021d8288(1);
    return native_fn_ov006_021da9d0();
}

/* 0x021da9d0: write the status panel labels for the active menu page. */
void native_ov006_021da9d0(void) {
    u8 *format = native_data_021c9698;
    u16 text[32];
    u8 *state;

    if (native_fn_02067748()[0x10] == 0) {
        native_fn_ov006_021d79e4(1, 15, 2, 126);
    } else {
        state = native_fn_02067748();
        native_fn_02046af4(format, (u32)(state + 16), 31, 0, (u8 *)text, 255);
        native_fn_ov006_021d7ad0(1, (u8 *)text);
    }
    if (*(u16 *)native_fn_0206442c() != 0) {
        native_fn_ov006_021d79f8(2, 15, 15, *(u16 *)native_fn_0206442c(), 16);
        native_fn_ov006_021d7e34();
        native_fn_ov006_021d7ebc(native_fn_020643fc(*(u16 *)native_fn_0206442c()), 14, 3);
    } else {
        native_fn_ov006_021d79e4(2, 15, 15, *(u16 *)native_fn_0206442c());
    }
    native_fn_02067dd4();
    native_fn_ov006_021d79e4(4, 15, 2, (u16)(native_fn_02067d54() + 164));
}

/* 0x021dafbc: draw the one-line hint panel from the two-record table. */
void native_ov006_021dafbc(void) {
    u8 text[1024];
    native_fn_ov006_021d7860();
    native_fn_ov006_021d77f8(11);
    native_fn_ov006_021d7d28(native_data_ov006_0220cb98, 2);
    native_fn_ov006_021d79e4(0, 15, 2, 88);
    native_fn_02046af4(native_data_021c9698, native_fn_0206784c(), 28, 0, text, 255);
    native_fn_ov006_021d7ad0(1, text);
}
