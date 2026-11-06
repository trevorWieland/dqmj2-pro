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
extern u32 native_fn_02008064();
extern u32 native_fn_0200e964();
extern u32 native_fn_0200f0a4();
extern u32 native_fn_0200f0c4();
void native_main_0200f278(void) {
    native_fn_02008064(0x360000);
    if (native_fn_0200f0c4() == 1) {
        return;
    }
    if (native_fn_0200e964(2, 0) != 0) {
        do {
            native_fn_02008064(0xA3A47);
        } while (native_fn_0200e964(2, 0) != 0);
    }
    if (native_fn_0200f0a4(1) != 0) {
        return;
    }
    do {
        native_fn_02008064(0xA);
    } while (native_fn_0200f0a4(1) == 0);
}
