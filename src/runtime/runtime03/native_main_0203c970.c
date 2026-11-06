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
extern u32 native_fn_0203c578();
extern u32 native_fn_0203c864();
extern u32 native_fn_0203c8e0();
extern u32 native_fn_0203c908();
extern u32 native_fn_0203c914();
extern u32 native_fn_0203c920();
extern u32 native_fn_0203c92c();
extern u32 native_fn_0203c940();
extern u32 native_fn_0203c94c();
extern u32 native_fn_0203c958();
extern u32 native_fn_0203c964();
extern u8 native_data_020f5f28[];
u32 native_main_0203c970(void) {
    native_fn_0203c578(0, native_data_020f5f28, 0x40, 0);
    native_fn_0203c864(0, native_fn_0203c8e0);
    native_fn_0203c864(1, native_fn_0203c908);
    native_fn_0203c864(2, native_fn_0203c914);
    native_fn_0203c864(3, native_fn_0203c920);
    native_fn_0203c864(4, native_fn_0203c92c);
    native_fn_0203c864(5, native_fn_0203c940);
    native_fn_0203c864(6, native_fn_0203c94c);
    native_fn_0203c864(7, native_fn_0203c958);
    return native_fn_0203c864(8, native_fn_0203c964);
}
