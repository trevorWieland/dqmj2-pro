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
extern u32 native_fn_02046af4();
extern u32 native_fn_02049ad0();
extern u32 native_fn_02049ae4();
extern u32 native_fn_02049f14();
extern u32 native_fn_02049f24();
extern u32 native_fn_020853c8();
extern u32 native_fn_ov006_021df15c();
extern u8 native_data_021c9698[];
u32 native_ov006_021def84(void) {
    u32 temp_r0;
    u32 temp_r4;
    u32 temp_r5;
    void *temp_r6;

    temp_r6 = M2C_FIELD(*(void **) native_fn_02049ad0((s8) (native_fn_ov006_021df15c() + 5)), void **, 4);
    temp_r5 = native_fn_02049f24();
    temp_r4 = native_fn_02049ae4();
    native_fn_02046af4(native_data_021c9698, M2C_FIELD(temp_r6, s32 *, 0x68), M2C_FIELD(temp_r6, u8 *, 0x5E), 0, temp_r5, 0xFF);
    temp_r0 = native_fn_02049f14(temp_r5);
    if (M2C_FIELD(temp_r4, s32 *, 0) == 0) {
        return temp_r0;
    }
    return native_fn_020853c8(M2C_FIELD(temp_r4, s32 *, 4));
}
