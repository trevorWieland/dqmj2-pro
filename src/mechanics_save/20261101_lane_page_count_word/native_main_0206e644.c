typedef signed char s8;
typedef unsigned int u32;
extern u32 native_fn_0206e2fc(u32, u32, u32, u32, u32);
extern u32 native_fn_0206e388(s8, s8);
extern u32 native_fn_0206e634(u32);
u32 native_main_0206e644(u32 value) {
    native_fn_0206e2fc(0, 0, 0x15, 0, 0);
    native_fn_0206e2fc(1, 0x1F, 0x15, 1, 0);
    native_fn_0206e388(4, 5);
    return native_fn_0206e634(value);
}
