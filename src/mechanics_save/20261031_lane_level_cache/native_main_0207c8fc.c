typedef unsigned int u32;
extern void *native_data_021c6758[20];
extern const char native_data_020de4e8[];
extern void *native_fn_0202a37c(u32, u32, int);
extern u32 native_fn_0202a818(const char *, void *, u32, u32);
extern void native_fn_0202a498(u32, void *);

u32 native_main_0207c8fc(u32 heap) {
    int index;
    u32 count;
    count = 0;
    index = 0;
    do {
        if (native_data_021c6758[index]) {
            native_fn_0202a498(heap, native_data_021c6758[index]);
            native_data_021c6758[index] = 0;
            count += 1;
        }
        index += 1;
    } while (index < 20);
    return count;
}
