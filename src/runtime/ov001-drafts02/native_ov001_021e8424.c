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
extern u32 native_fn_0207afec();
extern u32 ov001_side_slot_record_021db438();
extern u32 native_fn_ov001_021e2b88();
extern u32 native_fn_ov001_021e6a6c();
extern u32 native_fn_ov001_021e81d0();
void native_ov001_021e8424(s32 arg0, u32 arg1) {
    s32 var_r0;
    u32 temp_r4;
    u32 temp_r5;
    u32 temp_r6;
    u32 temp_r7;

    temp_r4 = ov001_side_slot_record_021db438();
    temp_r5 = ov001_side_slot_record_021db438(arg0, 0);
    if (arg0 == 0) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    temp_r6 = ov001_side_slot_record_021db438(var_r0, 0);
    temp_r7 = native_fn_ov001_021e81d0(arg0, arg1);
    if ((M2C_FIELD(temp_r4, u8 *, 0x322) != 0) && (arg0 != 0)) {

    } else if (((M2C_FIELD(temp_r7, u8 *, 4) == 0) || ((s32) native_fn_ov001_021e2b88() >= 2)) && (M2C_FIELD(temp_r7, u16 *, 0) != 6) && ((M2C_FIELD((void *) native_fn_0207afec(), s8 *, 0x26) == 0) || (M2C_FIELD(temp_r4, s8 *, 0x237) != 0))) {
        native_fn_ov001_021e6a6c(temp_r4, temp_r5, temp_r6, temp_r7, temp_r7 + 2, temp_r7 + 3, 1);
    }
    if (M2C_FIELD(temp_r4, u8 *, 0x322) == 1) {
        M2C_FIELD(temp_r4, u8 *, 0x35B) = (u8) (M2C_FIELD(temp_r4, u8 *, 0x35B) + 1);
    }
}
