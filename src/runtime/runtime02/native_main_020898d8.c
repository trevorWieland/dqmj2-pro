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
extern u32 native_fn_020649e8();
extern u32 native_fn_02089994();
extern u32 native_fn_02089a14();
u32 native_main_020898d8(s32 arg0) {
    s32 var_r5;
    void *temp_r0;
    void *temp_r0_2;

    var_r5 = 0;
loop_1:
    if (var_r5 < 3) {
        temp_r0 = (void *) native_fn_020649c0(var_r5);
        if ((s32) M2C_FIELD(temp_r0, s32 *, 0) > 0) {
            if (native_fn_02089994(M2C_FIELD(temp_r0, s16 *, 0x2E), M2C_FIELD(temp_r0, u8 *, 0x30)) == 1) {
                return 1U;
            }
            if (native_fn_02089a14(temp_r0 + 0xD6) == 1) {
                return 1U;
            }
            goto block_13;
        }
        goto block_13;
    }
    if (arg0 != 0) {
        temp_r0_2 = (void *) native_fn_020649e8(var_r5 - 3);
        if ((s32) M2C_FIELD(temp_r0_2, s32 *, 0) > 0) {
            if (native_fn_02089994(M2C_FIELD(temp_r0_2, s16 *, 0x2E), M2C_FIELD(temp_r0_2, u8 *, 0x30)) == 1) {
                return 1U;
            }
            if (native_fn_02089a14(temp_r0_2 + 0xD6) == 1) {
                return 1U;
            }
            goto block_13;
        }
    }
block_13:
    var_r5 += 1;
    if (var_r5 >= 6) {
        return 0U;
    }
    goto loop_1;
}
