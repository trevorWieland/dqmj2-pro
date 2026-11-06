typedef unsigned int u32;
extern u32 native_fn_020443ec(void);
u32 native_main_020444ec(void) {
    u32 mode = native_fn_020443ec();
    return mode == 2 || mode == 4;
}
