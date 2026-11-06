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
extern u32 native_fn_02028cec();
extern u32 native_fn_0203d294();
extern u32 native_fn_0204106c();
extern u32 native_fn_0204199c();
extern u32 native_fn_020430b4();
extern u8 native_data_020dd990[];
u32 native_main_02041e50(void *arg0, s16 arg1) {
    u32 var_r5;
    void *temp_r0;

    var_r5 = 0;
    if (M2C_FIELD(arg0, u8 *, 0x15C) == 0) {
        temp_r0 = (void *) native_fn_0204199c(M2C_FIELD((void *) native_fn_020430b4(arg1), s16 *, 2));
        if (M2C_FIELD(temp_r0, u8 *, 0x39) != 0) {
            native_fn_0204106c(arg0, temp_r0, 0);
            native_fn_02028cec(arg0, native_data_020dd990);
            M2C_FIELD(arg0, s16 *, 0x16A) = arg1;
            M2C_FIELD(arg0, s8 *, 0x15D) = (s8) *(u16 *) native_fn_020430b4(arg1);
            M2C_FIELD(arg0, s32 *, 0x164) = -1;
            M2C_FIELD(arg0, s16 *, 0x168) = -1;
            M2C_FIELD(arg0, s8 *, 0x160) = 0x1F;
            M2C_FIELD(arg0, s32 *, 0x7C) = 0x19A;
            M2C_FIELD(arg0, s32 *, 0x80) = 0x19A;
            M2C_FIELD(arg0, s32 *, 0x84) = 0x19A;
            M2C_FIELD(arg0, s8 *, 0x161) = (s8) native_fn_0203d294(8);
            var_r5 = 1;
            M2C_FIELD(arg0, s8 *, 0x15E) = 1;
            M2C_FIELD(arg0, s32 *, 0x16C) = 0x1000;
            M2C_FIELD(arg0, s16 *, 0x170) = 0;
            M2C_FIELD(arg0, s16 *, 0x172) = 0;
            M2C_FIELD(arg0, s16 *, 0x174) = 0;
            M2C_FIELD(arg0, s16 *, 0x176) = 0;
            M2C_FIELD(arg0, s8 *, 0x1DD) = 0;
            M2C_FIELD(arg0, s8 *, 0x1DF) = 1;
            M2C_FIELD(arg0, u8 *, 0x15C) = 1U;
        }
    }
    return var_r5;
}
