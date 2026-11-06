typedef unsigned int u32;
extern void *native_fn_02062a10(u32);
extern void native_fn_02008e0c(const void *, void *, u32);
int native_main_02062e18(u32 id, const void *input) {
    void *record = native_fn_02062a10(id);
    if (!record) return 0;
    native_fn_02008e0c(input, record, 20);
    return 1;
}
