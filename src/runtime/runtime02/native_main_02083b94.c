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
extern u32 native_fn_020136b4();
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u32 native_fn_02083420();
extern u8 native_data_021c72a0[];
extern u8 native_data_021c7ee0[];
u32 native_main_02083b94(void) {
    u32 temp_r0;

    if ((M2C_FIELD(native_data_021c72a0, s32 *, 0x34) == 5) && (native_fn_020136b4(native_data_021c7ee0) != 0)) {
        native_fn_020824c4();
    }
    temp_r0 = native_fn_02083420();
    if (temp_r0 != 0) {
        return temp_r0;
    }
    return native_fn_020824b4(0xA);
}
