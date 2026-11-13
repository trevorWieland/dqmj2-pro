typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_02044f9c();
extern u32 native_fn_020630b0();
extern u32 native_fn_0207c958();
extern u32 native_fn_0207c9b8();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021e485c();
extern u32 native_fn_ov001_022071a8();
extern u32 native_fn_ov001_022071d0();
typedef struct {
    u8 unknown_0[0x30];
    s32 field_30;
} Record_native_data_ov001_02238cd4;
extern Record_native_data_ov001_02238cd4 native_data_ov001_02238cd4;
u32 native_ov001_021e49d0(void) {
    s32 temp_r0;
    u8 temp_r1_2;
    void *temp_r1;
    s32 slot_index;
    u32 curve_id;
    u32 new_level;
    u32 actor;
    u32 any_level_up;

    any_level_up = 0;
    slot_index = 0;
    do {
        actor = ov001_side_slot_record_021db438(0, slot_index);
        if (ov001_record_is_active_021db8d0(actor) != 0) {
            M2C_FIELD(actor, s32 *, 0x200) = (s32) (M2C_FIELD(actor, s32 *, 0x200) + native_data_ov001_02238cd4.field_30);
            temp_r1 = M2C_FIELD(actor, void **, 0x1E8);
            curve_id = native_fn_02044f9c(M2C_FIELD(temp_r1, s16 *, 0x2A), M2C_FIELD(temp_r1, u8 *, 0x2C));
            temp_r0 = (s32) native_fn_0207c9b8(curve_id, native_fn_020630b0(M2C_FIELD(M2C_FIELD(actor, void **, 0x1E8), u8 *, 0xAB)));
            if ((s32) M2C_FIELD(actor, s32 *, 0x200) > temp_r0) {
                M2C_FIELD(actor, s32 *, 0x200) = temp_r0;
            }
            new_level = native_fn_0207c958(curve_id, M2C_FIELD(actor, s32 *, 0x200), M2C_FIELD(M2C_FIELD(actor, void **, 0x1E8), u8 *, 0xAB));
            temp_r1_2 = M2C_FIELD(actor, u8 *, 0x1FC);
            if (new_level > (u32) temp_r1_2) {
                native_fn_ov001_021e485c(actor, temp_r1_2, new_level, 1);
                native_fn_ov001_022071a8(slot_index, new_level);
                any_level_up = 1;
            } else {
                native_fn_ov001_022071d0(slot_index);
            }
            M2C_FIELD(actor, u32 *, 0x204) = native_fn_0207c9b8(curve_id, new_level + 1);
        }
        slot_index += 1;
    } while (slot_index < 3);
    return any_level_up;
}
