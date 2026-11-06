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
extern u32 native_fn_020649c0();
extern u32 native_fn_0207c2b8();
u32 native_main_020435e8(void) {
    s32 var_r6;
    u32 var_r7;
    void *temp_r0;

    var_r7 = 0;
    var_r6 = 0;
    do {
        temp_r0 = (void *) native_fn_020649c0(var_r6);
        if ((s32) M2C_FIELD(temp_r0, s16 *, 0x2E) >= 0) {
            M2C_FIELD(temp_r0, s16 *, 0x32) = (s16) native_fn_0207c2b8(temp_r0 + 0x11C, temp_r0 + 0x4A);
            M2C_FIELD(temp_r0, s8 *, 0xAA) = 0x32;
            var_r7 += 1;
        }
        var_r6 += 1;
    } while (var_r6 < 3);
    return var_r7;
}
