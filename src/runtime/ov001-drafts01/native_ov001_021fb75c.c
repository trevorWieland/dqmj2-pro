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
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
typedef struct {
    u8 unknown_0[0x40];
    s32 field_40;
} Record_native_data_ov001_02239a14;
extern Record_native_data_ov001_02239a14 native_data_ov001_02239a14;
u32 native_ov001_021fb75c(void) {
    s32 var_r8;
    u32 temp_r6;
    u32 var_r0;

    var_r8 = 0;
    do {
        var_r0 = ov001_side_slot_record_021db438(1, var_r8);
        temp_r6 = var_r0;
        if ((temp_r6 != 0) && (temp_r6 != native_data_ov001_02239a14.field_40)) {
            var_r0 = ov001_record_is_active_021db8d0();
            if (var_r0 != 0) {
                M2C_FIELD(temp_r6, s8 *, 0x325) = 1;
            }
        }
        var_r8 += 1;
    } while (var_r8 < 3);
    return var_r0;
}
