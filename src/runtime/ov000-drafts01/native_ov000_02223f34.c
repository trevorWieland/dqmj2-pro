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
extern u32 native_fn_01ffa010();
extern u32 native_fn_01ffa8c8();
extern u32 native_fn_01ffa8d8();
extern u32 native_fn_01ffb4ec();
extern u32 native_fn_0203d294();
extern u32 native_fn_0203d2ec();
extern u32 native_fn_ov000_02223fa8();
extern u32 native_fn_ov000_02224420();
u32 native_ov000_02223f34(void) {
    s32 var_r5;
    s8 temp_r3;
    u32 temp_r4;
    u32 temp_r6;
    void *temp_r0;

    temp_r6 = native_fn_01ffa8d8();
    native_fn_01ffa8c8();
    native_fn_0203d2ec();
    native_fn_ov000_02224420();
    var_r5 = 0;
    do {
        temp_r4 = native_fn_01ffb4ec((u8) native_fn_0203d294(temp_r6));
        temp_r0 = (void *) native_fn_01ffb4ec((u8) native_fn_0203d294(temp_r6));
        var_r5 += 1;
        temp_r3 = M2C_FIELD(temp_r4, s8 *, 0x165);
        M2C_FIELD(temp_r4, s8 *, 0x165) = (s8) M2C_FIELD(temp_r0, s8 *, 0x165);
        M2C_FIELD(temp_r0, s8 *, 0x165) = temp_r3;
    } while (var_r5 < 0x10);
    return native_fn_ov000_02223fa8(*(s8 *) native_fn_01ffa010());
}
