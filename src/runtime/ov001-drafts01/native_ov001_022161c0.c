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
extern u32 native_fn_0205c904();
extern u32 ov001_side_slot_record_021db438();
extern u32 ov001_record_is_active_021db8d0();
extern u32 ov001_effect_resource_create_021eec7c();
u32 native_ov001_022161c0(void) {
    s32 var_r9;
    u32 temp_r7;
    u32 var_r0;

    var_r9 = 0;
    do {
        temp_r7 = ov001_side_slot_record_021db438(0, var_r9);
        var_r0 = ov001_record_is_active_021db8d0();
        if (var_r0 != 0) {
            native_fn_0205c904(0x83);
            var_r0 = ov001_effect_resource_create_021eec7c(0x83, temp_r7, 1);
        }
        var_r9 += 1;
    } while (var_r9 < 3);
    return var_r0;
}
