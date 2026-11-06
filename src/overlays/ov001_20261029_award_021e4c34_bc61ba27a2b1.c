typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_02008d78();
extern u32 native_fn_02044f9c();
extern u32 native_fn_02062b00();
extern u32 native_fn_020630b0();
extern u32 native_fn_020634cc();
extern u32 native_fn_02063c00();
extern u32 native_fn_0207c8a4();
extern u32 native_fn_0207c958();
extern u32 native_fn_0207c9b8();
extern u32 native_fn_ov001_021d8d1c();
extern u32 native_fn_ov001_021e4120();
extern u32 native_fn_ov001_021e46d8();
extern u32 native_fn_ov001_021e4ac4();
extern u32 native_fn_ov001_021e4afc();
typedef struct {
    u8 unknown_0[0x38];
    s32 field_38;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e4c34(void) {
    s32 temp_r0;
    s32 temp_r0_3;
    s32 temp_r0_5;
    s32 temp_r0_6;
    u32 curve_id;
    u8 temp_r0_4;
    s32 var_r1;
    u8 temp_r1;
    s32 temp_r4;
    s32 skill_count;
    u32 record;
    u32 new_level;
    s16 growth[8];
    s32 record_index;
    u32 awarded_count;

    awarded_count = 0;
    record = native_fn_02062b00();
    record_index = 0;
    do {
        temp_r4 = M2C_FIELD(record, s32 *, 0x14);
        if ((temp_r4 != 0) && (native_fn_ov001_021e4ac4(temp_r4) == 0)) {
            if ((native_fn_ov001_021e4afc(temp_r4) == 0) && (M2C_FIELD(record, u8 *, 0x33) == 0)) {
                M2C_FIELD(record, s32 *, 0x34) = (s32) (M2C_FIELD(record, s32 *, 0x34) + ((native_data_ov001_02238cd4.field_38 + 0x17) / 24));
                curve_id = native_fn_02044f9c(M2C_FIELD(record, s16 *, 0x18), M2C_FIELD(record, u8 *, 0x1A));
                native_fn_0207c8a4(1, curve_id);
                temp_r0_3 = (s32) native_fn_0207c9b8(curve_id, native_fn_020630b0(M2C_FIELD(record, u8 *, 0x1C)));
                if ((s32) M2C_FIELD(record, s32 *, 0x34) > temp_r0_3) {
                    M2C_FIELD(record, s32 *, 0x34) = temp_r0_3;
                }
                new_level = native_fn_0207c958(curve_id, M2C_FIELD(record, s32 *, 0x34), M2C_FIELD(record, u8 *, 0x1C));
                skill_count = 0;
                var_r1 = 0;
                do {
                    temp_r0_4 = M2C_FIELD((record + (var_r1 * 2)), u8 *, 0x7A);
                    var_r1 += 1;
                    if (temp_r0_4 != 0) {
                        skill_count += 1;
                    }
                } while (var_r1 < 5);
                if (new_level > (u32) M2C_FIELD(record, u8 *, 0x30)) {
                    do {
                        ++M2C_FIELD(record, u8 *, 0x30);
                        native_fn_02008d78(growth, 0, 0x10);
                        native_fn_ov001_021e4120(growth, M2C_FIELD(record, s32 *, 0x14), M2C_FIELD(record, u8 *, 0x30));
                        M2C_FIELD(record, s16 *, 0x20) = (s16) (M2C_FIELD(record, s16 *, 0x20) + growth[0]);
                        M2C_FIELD(record, s16 *, 0x22) = (s16) (M2C_FIELD(record, s16 *, 0x22) + growth[1]);
                        M2C_FIELD(record, s16 *, 0x28) = (s16) (M2C_FIELD(record, s16 *, 0x28) + growth[2]);
                        M2C_FIELD(record, s16 *, 0x2A) = (s16) (M2C_FIELD(record, s16 *, 0x2A) + growth[3]);
                        M2C_FIELD(record, s16 *, 0x2C) = (s16) (M2C_FIELD(record, s16 *, 0x2C) + growth[4]);
                        M2C_FIELD(record, s16 *, 0x2E) = (s16) (M2C_FIELD(record, s16 *, 0x2E) + growth[5]);
                        temp_r0_5 = skill_count * native_fn_ov001_021d8d1c(M2C_FIELD(record, u8 *, 0x30));
                        temp_r0_6 = (temp_r0_5 + 4) / 5;
                        M2C_FIELD(record, s16 *, 0x3C) = (s16) (M2C_FIELD(record, s16 *, 0x3C) + temp_r0_6);
                        if ((s32) M2C_FIELD(record, s16 *, 0x3C) > 0x3E7) {
                            M2C_FIELD(record, s16 *, 0x3C) = 0x3E7;
                        }
                        if (temp_r0_6 > 0) {
                            native_fn_02063c00(0x13, 1);
                        }
                        native_fn_ov001_021e46d8((void *) record, growth);
                        M2C_FIELD(record, s16 *, 0x24) = (s16) (M2C_FIELD(record, s16 *, 0x24) + growth[0]);
                        M2C_FIELD(record, s16 *, 0x26) = (s16) (M2C_FIELD(record, s16 *, 0x26) + growth[1]);
                        temp_r1 = M2C_FIELD(record, u8 *, 0x30);
                        if (new_level <= (u32) temp_r1) {
                            M2C_FIELD(record, u32 *, 0x38) = native_fn_020634cc(M2C_FIELD(record, s16 *, 0x18), M2C_FIELD(record, u8 *, 0x1A), temp_r1 + 1);
                        }
                    } while (new_level > (u32) M2C_FIELD(record, u8 *, 0x30));
                }
                awarded_count += 1;
            }
        }
        record += 0x84;
        temp_r0 = record_index + 1;
        record_index = temp_r0;
    } while (temp_r0 < 0x64);
    return awarded_count;
}
