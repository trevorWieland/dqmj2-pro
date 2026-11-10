/*
 * ov006 packet p4-1: menu record layout and hint panels.
 *
 * native_data_ov006_0220f2f4.field_4 points at a 0x100-byte staging block
 * holding five 0x30-byte UI rows; each row copies a small header from the
 * runtime character record returned by 0x02067bd4.
 */
#include "context.h"

typedef struct {
    u8 reserved0[4];
    s32 field_4; /* 0x04: staging block base */
} Record_native_data_ov006_0220f2f4;

extern Record_native_data_ov006_0220f2f4 native_data_ov006_0220f2f4;

extern u32 native_fn_02067b48(void);
extern u32 native_fn_02067bd4(s32 row);
extern u32 native_fn_02067bec(u32 a, s32 index);
extern u32 native_fn_ov006_021da064(void);
extern u32 native_fn_ov006_021de288(s32 row);

/* 0x021da2c8: refill the five rows from the active character records. */
u32 native_ov006_021da2c8(void) {
    u32 record;
    u32 header;
    s32 row;
    s32 offset;

    native_fn_02008d78((u8 *)native_data_ov006_0220f2f4.field_4, 0, 0x100);
    row = 0;
    offset = 0;
    do {
        header = native_fn_02067bd4(row);
        native_fn_02008e0c((u8 *)(header + 0x14),
                           (u8 *)(native_data_ov006_0220f2f4.field_4 + 0x10 + offset), 0x18);
        *(s32 *)(native_data_ov006_0220f2f4.field_4 + offset + 0x30) = *(s32 *)(header + 0xC);
        *(s32 *)(native_data_ov006_0220f2f4.field_4 + offset + 0x28) = *(s32 *)(header + 0);
        *(s32 *)(native_data_ov006_0220f2f4.field_4 + offset + 0x30) = *(s32 *)(header + 0xC);
        *(s32 *)(native_data_ov006_0220f2f4.field_4 + offset + 0x2C) = *(s32 *)(header + 8);
        *(s16 *)(native_data_ov006_0220f2f4.field_4 + offset + 0x3E) = (s16)native_fn_ov006_021de288(row);
        native_fn_02067bec(row, 0);
        *(s16 *)(native_data_ov006_0220f2f4.field_4 + offset + 0x3C) = (s16)native_fn_ov006_021da064();
        record = native_fn_02067b48();
        *(u32 *)(native_data_ov006_0220f2f4.field_4 + offset + 0x38) = record;
        row++;
        offset += 0x30;
    } while (row < 5);
    return record;
}
