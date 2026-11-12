typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
extern u32 native_fn_0203d294();
extern u32 native_fn_0207afec();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 native_fn_ov001_021e1358();
extern u32 native_fn_ov001_021f1294();
extern u32 ov001_begin_state_transition_021f1354();
extern u32 ov001_select_mode_id_021f1438();
extern u32 native_fn_ov001_021f2304();
extern u32 native_fn_ov001_021f2550();
extern u32 native_fn_ov001_0220f9a4();
extern u8 native_data_ov001_0223989c[];
extern u8 native_data_ov001_022398ae[];
u32 native_ov001_021f2698(void) {
    u32 temp_r5;
    u32 var_r6;
    void *temp_r0;

    if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 2) {
        native_fn_ov001_021f1294(0x10, 2);
    }
    native_fn_ov001_021e1358(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x80), u8 *, 0x31E));
    M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x21) = 0;
    if (((u32) (M2C_FIELD((void *) native_fn_0207afec(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50)), u16 *, 8) << 0x18) >> 0x1C) == 4) {
        do {
            temp_r5 = ov001_side_slot_record_021db438(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x80), u8 *, 0x31E), native_fn_0203d294(3));
        } while (ov001_record_is_active_021db8d0() == 0);
        M2C_FIELD(native_data_ov001_0223989c, void **, 0x80) = (void *) temp_r5;
    }
    if (((u32) (M2C_FIELD((void *) native_fn_0207afec(M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50)), u16 *, 8) << 0x10) >> 0x1C) == 0) {
        M2C_FIELD(native_data_ov001_0223989c, void **, 0x80) = (void *) ov001_side_slot_record_021db438(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x80), u8 *, 0x31E), native_fn_ov001_021f2304(M2C_FIELD(native_data_ov001_0223989c, void **, 0x80), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x10)));
    }
    var_r6 = 0;
    do {
        temp_r0 = ov001_side_slot_record_021db438(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x80), u8 *, 0x31E), var_r6) + 0x300;
        var_r6 += 1;
        M2C_FIELD(temp_r0, s16 *, 0x4A) = 0;
    } while ((s32) var_r6 < 3);
    if ((native_fn_ov001_0220f9a4(M2C_FIELD(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), s32 *, 0x1E8) + 0x46, M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50), native_data_ov001_022398ae) != 0) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 3)) {
        M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 0x18;
        if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) == 1) {
            ov001_begin_state_transition_021f1354(M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xE), M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x23), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x4E), 1);
        }
    } else if ((M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 2) && (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) != 3)) {
        M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x29) = (s8) native_fn_ov001_021f2550(M2C_FIELD(native_data_ov001_0223989c, void **, 0x84), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x50));
        M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 1;
    } else {
        if (M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x35) == 3) {
            ov001_begin_state_transition_021f1354(M2C_FIELD(native_data_ov001_0223989c, u8 *, 0xE), M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x23), M2C_FIELD(native_data_ov001_0223989c, u16 *, 0x4E), 1);
            ov001_select_mode_id_021f1438(M2C_FIELD(native_data_ov001_0223989c, u8 *, 0x15));
        }
        M2C_FIELD(native_data_ov001_0223989c, s8 *, 0x1B) = 3;
    }
    return 1U;
}
