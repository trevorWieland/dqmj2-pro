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
extern u32 native_fn_020443d4();
extern u32 native_fn_0205bd60();
extern u32 native_fn_02064978();
extern u32 native_fn_02064b24();
extern u32 native_fn_02064c8c();
extern u32 native_fn_02064d64();
extern u32 native_fn_02065170();
extern u32 native_fn_020652dc();
extern u32 native_fn_02065304();
extern u32 native_fn_0206532c();
extern u32 native_fn_0206534c();
extern u32 native_fn_020655c8();
extern u32 native_fn_02065630();
extern u32 native_fn_02065648();
extern u32 native_fn_020656b0();
extern u32 native_fn_020656d0();
u32 native_ov000_0222b708(void) {
    s8 temp_r5;
    void *temp_r4;

    temp_r4 = (void *) native_fn_0205bd60();
    temp_r5 = M2C_FIELD(temp_r4, s8 *, 0x11);
    native_fn_02064978();
    native_fn_020443d4(7);
    native_fn_020652dc(M2C_FIELD(temp_r4, u8 *, 0xD));
    native_fn_02065304(0);
    native_fn_02065630(0);
    native_fn_0206534c(-1);
    native_fn_0206532c(3);
    native_fn_02065648(M2C_FIELD(temp_r4, u8 *, 0x12));
    native_fn_020656b0(0);
    native_fn_020655c8(0);
    native_fn_020656d0(1);
    native_fn_02064b24(-1, -1, -1);
    native_fn_02064c8c(-1, -1, -1);
    native_fn_02064d64(temp_r5, -1, -1);
    native_fn_02065170(-1, -1, -1);
    return 0U;
}
