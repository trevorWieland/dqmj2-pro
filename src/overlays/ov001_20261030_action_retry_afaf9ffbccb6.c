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
#define NULL ((void *)0)
extern u32 native_fn_0203d294();
extern u32 ov001_side_slot_record_021db438(s32, u32);
extern u32 native_fn_ov001_021e7290();
extern u32 native_fn_ov001_021e7484();
extern u32 native_fn_ov001_021e81d0();
void native_ov001_021e8510(s32 arg0, u32 arg1) {
    s32 var_r0;
    s8 temp_r0;
    u32 temp_r0_2;
    u8 temp_r0_3;
    void *temp_r0_4;
    s8 var_r1;
    u32 temp_r7;
    u32 temp_r8;
    u32 temp_r9;
    s32 var_r10;

    var_r10 = 0;
    temp_r0_4 = (void *) ov001_side_slot_record_021db438(arg0, arg1);
    temp_r0_3 = M2C_FIELD(temp_r0_4, u8 *, 0x322);
    if (temp_r0_3 != 1) {
        return;
    }
    temp_r7 = ov001_side_slot_record_021db438(arg0, 0);
    if (arg0 == 0) {
        var_r0 = 1;
    } else {
        var_r0 = 0;
    }
    temp_r8 = ov001_side_slot_record_021db438(var_r0, 0);
    temp_r9 = native_fn_ov001_021e81d0(arg0, arg1);
loop_6:
    native_fn_ov001_021e7290(temp_r0_4, temp_r7, temp_r8, temp_r9, temp_r9 + 2, temp_r9 + 3);
    temp_r0_2 = native_fn_ov001_021e7484(temp_r0_4, M2C_FIELD(temp_r9, u16 *, 0));
    if (temp_r0_2 != 0) {
        return;
    }
    var_r10 += 1;
    M2C_FIELD(temp_r0_4, u8 *, 0x35B) = (u8) (M2C_FIELD(temp_r0_4, u8 *, 0x35B) + 1);
    if (var_r10 > 0x20) {
        var_r1 = 0;
        M2C_FIELD(temp_r9, u16 *, 0) = 0U;
        if (M2C_FIELD(temp_r0_4, u8 *, 0x31E) == 0) {
            var_r1 = 1;
        }
        M2C_FIELD(temp_r9, s8 *, 2) = var_r1;
        temp_r0 = (s8) native_fn_0203d294(3);
        M2C_FIELD(temp_r9, s8 *, 3) = temp_r0;
        return;
    }
    goto loop_6;
}
