typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef s32 (*NativeCompare)(const u32 *, const u32 *);
extern u32 *native_data_021c67a8;
extern const u8 *native_fn_02062b00(void);
extern void native_fn_0201d470(void *, u32, u32, NativeCompare);
extern s32 native_fn_0207cb3c(const u32 *, const u32 *);
extern s32 native_fn_0207cbec(const u32 *, const u32 *);
extern s32 native_fn_0207cc74(const u32 *, const u32 *);
extern s32 native_fn_0207cd04(const u32 *, const u32 *);

u32 native_main_0207ca3c(u32 mode) {
    const u8 *record;
    s32 index;
    switch (mode) {
    case 0:
        record = native_fn_02062b00();
        index = 0;
        do {
            native_data_021c67a8[index] = *(const u32 *)(record + 20);
            record += 132;
            index += 1;
        } while (index < 100);
        break;
    case 1:
        native_main_0207ca3c(0);
        native_fn_0201d470(native_data_021c67a8, 100, 4, native_fn_0207cb3c);
        break;
    case 2:
        native_main_0207ca3c(0);
        native_fn_0201d470(native_data_021c67a8, 100, 4, native_fn_0207cbec);
        break;
    case 3:
        native_main_0207ca3c(0);
        native_fn_0201d470(native_data_021c67a8, 100, 4, native_fn_0207cc74);
        break;
    case 4:
        native_main_0207ca3c(0);
        native_fn_0201d470(native_data_021c67a8, 100, 4, native_fn_0207cd04);
    default:
        return 0;
    }
    return 1;
}
