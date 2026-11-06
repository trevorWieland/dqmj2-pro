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
extern u32 native_fn_02048f7c();
extern u32 native_fn_02049ad0();
extern u32 native_fn_02068f60();
extern u32 native_fn_020c483c();
extern u32 native_fn_020c484c();
extern u32 native_fn_020c4870();
extern u32 native_fn_020c48bc();
extern u32 native_fn_020c48d0();
extern u32 native_fn_020c48e8();
extern u8 native_data_021d63c8[];
u32 native_main_020c8ef0(void) {
    void *temp_r0;
    u32 var_r4;
    s32 var_r5;

    var_r4 = 0;
    var_r5 = 1;
    switch (M2C_FIELD(native_data_021d63c8, s8 *, 0x10)) {
    case 0:
        temp_r0 = M2C_FIELD(*(void **) native_fn_02049ad0((s8) (M2C_FIELD(native_data_021d63c8, s32 *, 0) + 0xD)), void **, 4);
        native_fn_020c4870(M2C_FIELD(temp_r0, s32 *, 0x64), M2C_FIELD(temp_r0, u16 *, 0x6C));
        native_fn_020c48d0(9, 7, (u16) M2C_FIELD(native_data_021d63c8, s32 *, 0));
        break;
    case 1:
        native_fn_020c48bc();
        native_fn_020c483c(1);
        break;
    default:
        var_r5 = 0;
        break;
    }
    if (var_r5 != 0) {
        native_fn_020c48e8(0x57);
        native_fn_02048f7c(1);
        native_fn_020c484c();
        var_r4 = 1;
        native_fn_02068f60(0);
    }
    return var_r4;
}
