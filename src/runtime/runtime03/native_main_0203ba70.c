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
extern u32 native_fn_02009200();
extern u32 native_fn_020097b8();
extern u32 native_fn_02009974();
extern u32 native_fn_020099e0();
u32 native_main_0203ba70(void *arg0) {
    u32 temp_r4;

    if (((s32) (M2C_FIELD(arg0, s32 *, 0x24) << 0x1E) >> 0x1F) == 0) {
        return (u32) arg0;
    }
    native_fn_02009200(M2C_FIELD(arg0, s32 *, 0x44), 0, 1 << M2C_FIELD(arg0, s32 *, 0x40), 0);
    temp_r4 = native_fn_020099e0();
    native_fn_020097b8(1);
    return native_fn_02009974(temp_r4);
}
