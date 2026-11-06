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
extern u32 native_fn_02049ad0();
extern u32 native_fn_0204a010();
extern u32 native_fn_0207f0a8();
extern u32 native_fn_0207f148();
extern u32 native_fn_0207ff4c();
extern u8 native_data_020de57c[];
extern u8 native_data_021c6d80[];
extern u8 native_data_021c6d88[];
extern u8 native_data_021c6daa[];
u32 native_main_0207fe28(void) {
    s32 var_r8;
    s32 var_r9;
    u32 temp_r1;
    u8 *var_r10;

    if (M2C_FIELD(native_data_020de57c, u8 *, 0) != 1) {
        return (u32) M2C_FIELD(native_data_020de57c, u8 *, 0);
    }
    M2C_FIELD(native_data_020de57c, u8 *, 0) = 0;
    native_fn_0207f148(0, 0x10, 0, 0, native_data_021c6daa, 0, 0);
    native_fn_0204a010(M2C_FIELD(*(void **) native_fn_02049ad0(0), s32 *, 4), 0, 0x10, 0xE0, 0x10);
    var_r8 = 0;
    if ((s32) M2C_FIELD(native_data_020de57c, u8 *, 1) <= 0) {
        return (u32) M2C_FIELD(native_data_020de57c, u8 *, 1);
    }
    var_r10 = native_data_021c6d88;
    var_r9 = 0;
    do {
        if ((var_r8 != *native_data_021c6d80) || (native_fn_0207ff4c() == 1)) {
            temp_r1 = (M2C_FIELD(native_data_020de57c, u8 *, 1) * 0xA) + ((M2C_FIELD(native_data_020de57c, u8 *, 1) - 1) * 2);
            native_fn_0207f0a8(0, (s16) (var_r9 + (s16) (0x78 - ((s32) (temp_r1 + (temp_r1 >> 0x1F)) >> 1))), 0x10, 0, var_r10, 0);
        }
        var_r8 += 1;
        var_r9 += 0xC;
        var_r10 += 3;
    } while (var_r8 < (s32) M2C_FIELD(native_data_020de57c, u8 *, 1));
    return (u32) M2C_FIELD(native_data_020de57c, u8 *, 1);
}
