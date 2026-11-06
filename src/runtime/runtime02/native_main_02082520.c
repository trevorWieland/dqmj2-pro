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
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_02082584();
extern u32 native_fn_0208261c();
extern u8 native_data_021c72a0[];
u32 native_main_02082520(void *arg0) {
    u32 temp_r0;
    u32 temp_r0_2;

    if (M2C_FIELD(arg0, u16 *, 2) != 0) {
        native_fn_020824c4();
        return native_fn_020824b4(9);
    }
    if (M2C_FIELD(native_data_021c72a0, s32 *, 0x38) != 0) {
        temp_r0_2 = native_fn_02082584();
        if (temp_r0_2 != 0) {
            return temp_r0_2;
        }
        return native_fn_020824b4(9);
    }
    temp_r0 = native_fn_0208261c();
    if (temp_r0 != 0) {
        return temp_r0;
    }
    return native_fn_020824b4(9);
}
