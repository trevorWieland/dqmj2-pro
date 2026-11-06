typedef unsigned int u32;
extern void *native_data_021c6758[20];
extern const char native_data_020de4e8[];
extern void *native_fn_0202a37c(u32, u32, int);
extern u32 native_fn_0202a818(const char *, void *, u32, u32);
extern void native_fn_0202a498(u32, void *);

u32 native_main_0207c8a4(u32 heap, u32 index) {
    void *buffer;
    buffer = native_data_021c6758[index];
    if (!buffer) {
        buffer = native_fn_0202a37c(heap, 400, 4);
        if (buffer) {
            native_fn_0202a818(native_data_020de4e8, buffer, 400, index * 400);
            native_data_021c6758[index] = buffer;
        }
    }
    return (u32)buffer;
}
