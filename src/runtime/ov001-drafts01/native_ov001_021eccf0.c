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
extern u32 native_fn_0207b058();
extern u32 native_fn_0207d6c4();
extern u32 native_fn_0207d708();
extern u32 native_fn_0207d74c();
extern u32 native_fn_ov001_021d908c();
extern u32 native_fn_ov001_021ecc14();
extern u32 native_fn_ov001_02209490();
extern u8 native_data_ov001_02238d7c[];
u32 native_ov001_021eccf0(void *arg0, u32 arg1, u32 arg2) {
    u32 temp_r0;
    u32 temp_r4;
    u32 var_r1;
    u32 var_r8;

    var_r8 = 0;
    temp_r4 = native_fn_ov001_021ecc14(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x54), u8 *, 0x31E), 3, 8);
    if ((native_fn_0207d6c4(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD)) != 0) && (native_fn_0207b058(arg1, 0x40) != 0)) {
        temp_r0 = native_fn_0207d708(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD));
        if (temp_r0 == 0) {
            var_r1 = 0x64;
        } else {
            var_r1 = native_fn_ov001_021d908c(temp_r4, M2C_FIELD((M2C_FIELD(arg0, s32 *, 0x1E8) + temp_r0), u8 *, 0x86), native_fn_ov001_02209490(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x54) + 0x22C));
        }
        var_r8 = native_fn_0207d74c(M2C_FIELD(M2C_FIELD(native_data_ov001_02238d7c, void **, 0x60), u8 *, 0x1FD), var_r1, arg2);
    }
    return var_r8;
}
