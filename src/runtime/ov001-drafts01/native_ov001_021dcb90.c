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
u32 native_ov001_021dcb90(void) {
    s32 var_r2;
    s32 var_r2_2;
    u32 var_r0;
    u32 var_r0_2;

    var_r0_2 = ov001_side_slot_record_021db438(0, 0);
    var_r2 = 0;
    do {
        var_r2 += 1;
        M2C_FIELD(var_r0_2, s32 *, 0x33C) = 0;
        var_r0_2 += 0x440;
    } while (var_r2 < 3);
    var_r0 = ov001_side_slot_record_021db438(1);
    var_r2_2 = 0;
    do {
        var_r2_2 += 1;
        M2C_FIELD(var_r0, s32 *, 0x33C) = 0;
        var_r0 += 0x440;
    } while (var_r2_2 < 3);
    return var_r0;
}
