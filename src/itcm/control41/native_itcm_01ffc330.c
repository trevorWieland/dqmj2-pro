typedef unsigned int u32;
extern void native_fn_01ffbfbc(void);
extern void native_fn_01ffc324(void);
extern void native_fn_01ffc194(void);
extern void native_fn_01ffc184(void);
extern u32 native_fn_020ba848(u32, u32, u32, u32, u32, u32, u32 *, u32);
u32 native_itcm_01ffc330(u32 first, ...) {
    return native_fn_020ba848(2, (u32)native_fn_01ffbfbc, (u32)native_fn_01ffc324, (u32)native_fn_01ffc194,
                            (u32)native_fn_01ffc184, 0x2710, &first, 1);
}
