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
extern u32 native_fn_ov001_021e81d0();
extern u32 native_fn_ov001_0220f160();
extern u32 native_fn_ov001_0220f1c8();
u32 native_ov001_021e85f4(u32 arg0, u32 arg1) {
    s32 var_r0;
    u16 *temp_r0;
    u32 temp_r5;

    temp_r5 = ov001_side_slot_record_021db438();
    temp_r0 = (u16 *) native_fn_ov001_021e81d0(arg0, arg1);
    if (native_fn_ov001_0220f160(M2C_FIELD(temp_r5, s32 *, 0x1E8) + 0x46, *temp_r0) != 0) {
        if (M2C_FIELD(temp_r5, s8 *, 0x263) != 0) {
            var_r0 = 1;
        } else {
            var_r0 = 0;
        }
        return var_r0 + 2;
    }
    return native_fn_ov001_0220f1c8(temp_r5, *temp_r0);
}
