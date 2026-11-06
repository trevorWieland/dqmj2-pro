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
extern u32 native_fn_02048f1c();
extern u32 native_fn_02048f2c();
extern u32 native_fn_02048f3c();
extern u32 native_fn_02048f7c();
extern u32 native_fn_02049ad0();
extern u32 native_fn_0205fd80();
extern u32 native_fn_020c484c();
extern u32 native_fn_ov000_021ef5bc();
extern u32 native_fn_ov000_021efd88();
extern u32 native_fn_ov000_021efe1c();
extern u8 native_data_ov000_02236bc4[];
u32 native_ov000_021ec638(void) {
    s8 var_r7;
    void *temp_r0;

    native_fn_0205fd80(1);
    var_r7 = 0;
    do {
        temp_r0 = (void *) native_fn_02049ad0(var_r7);
        M2C_FIELD(temp_r0, s8 *, 4) = 0x7F;
        M2C_FIELD(temp_r0, s8 *, 5) = 0x7F;
        M2C_FIELD(temp_r0, s32 *, 0) = 0;
        var_r7 += 1;
        M2C_FIELD(temp_r0, s8 *, 6) = -1;
    } while ((s32) var_r7 < 0x24);
    native_fn_ov000_021ef5bc();
    native_fn_02048f1c(1, 1);
    native_fn_02048f2c(0, 1);
    native_fn_02048f3c(2, 1);
    native_fn_02048f7c(1);
    native_fn_020c484c();
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x100) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x102) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x103) = 0x7F;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x20) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x10) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x510) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s32 *, 0x514) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x518) = 0;
    M2C_FIELD(M2C_FIELD(native_data_ov000_02236bc4, void **, 4), s8 *, 0x50A) = 0;
    native_fn_ov000_021efe1c();
    return native_fn_ov000_021efd88();
}
