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
extern u32 native_fn_020273c8();
extern u32 native_fn_02027400();
extern u32 native_fn_02067cb4();
extern u32 native_fn_ov006_021e3cd8();
extern u32 native_fn_ov006_021e3f28();
extern u32 native_fn_ov006_021e6560();
extern u32 native_fn_ov006_021e802c();
extern u32 native_fn_ov006_021e938c();
u32 native_ov006_021e3d1c(void) {
    u32 temp_r0;
    u32 temp_r0_2;

    temp_r0 = native_fn_020273c8();
    switch (temp_r0) {
    case 3:
        temp_r0_2 = native_fn_02027400();
        switch (temp_r0_2) {
        case 15:
            native_fn_ov006_021e3f28(0x2E);
            native_fn_ov006_021e6560(1, 0);
            *(s32 *)0x04001000 = (*(s32 *)0x04001000 & ~0x1F00) | 0x300;
            break;
        case 9:
            native_fn_ov006_021e802c(0);
            native_fn_ov006_021e3f28(0x6D);
            break;
        case 8:
            native_fn_02067cb4(-1);
            native_fn_ov006_021e802c(1);
            native_fn_ov006_021e3f28(3);
            native_fn_ov006_021e938c(0x32);
            break;
        default:
            native_fn_02067cb4(-1);
            native_fn_ov006_021e802c(0);
            native_fn_ov006_021e3f28(3);
            native_fn_ov006_021e938c(0x32);
            break;
        }
        break;
    case 10:
        native_fn_ov006_021e802c(0);
        native_fn_ov006_021e3f28(0x56);
        native_fn_ov006_021e938c(0x32);
        break;
    }
    return native_fn_ov006_021e3cd8();
}
