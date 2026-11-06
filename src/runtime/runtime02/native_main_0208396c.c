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
extern u32 native_fn_02011f14();
extern u32 native_fn_020824b4();
extern u32 native_fn_020824c4();
extern u8 native_data_021c72a0[];
u32 native_main_0208396c(void *arg0) {
    if (M2C_FIELD(arg0, u16 *, 2) != 0) {
        native_fn_020824c4();
        return native_fn_020824b4(0xA);
    }
    if (native_fn_02011f14(M2C_FIELD(native_data_021c72a0, s32 *, 0x30)) != 0) {
        native_fn_020824c4();
        return native_fn_020824b4(0xA);
    }
    return native_fn_020824b4(1);
}
