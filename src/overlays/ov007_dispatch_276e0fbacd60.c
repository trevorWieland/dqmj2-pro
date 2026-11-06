typedef signed char s8;
typedef unsigned int u32;

extern u32 data_ov007_021daa10[];
extern s8 data_ov007_021da924;
extern u32 data_ov007_021da9d8[];
extern void func_0205be14(u32);
extern u32 func_02025a70(void);
extern u32 func_0204bd00(void *, u32);
extern u32 func_ov007_021d9858(void);
extern void func_02046150(u32, u32, u32);
extern void func_020462e0(u32, u32, u32);
extern u32 func_02084924(u32, u32, u32, u32, u32, u32, u32, u32, u32, u32);
extern void func_02085270(void *, u32, u32);

u32 native_ov007_021d96b0(u32 code) {
    switch (code) {
        case 128:
            break;
        case 140:
            func_0205be14(code);
            data_ov007_021daa10[276] = func_02025a70();
            break;
        case 129:
            func_0205be14(code);
            data_ov007_021daa10[276] = func_02025a70();
            break;
        default:
            return 0;
    }
    return func_0204bd00(data_ov007_021daa10, code);
}

u32 native_ov007_021d9c3c(void) {
    switch (data_ov007_021da924) {
        case 0:
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        case 8:
        case 9:
            if (func_ov007_021d9858() == 0) {
                return 0;
            }
            data_ov007_021da924 = -1;
            return 1;
    }
    return 1;
}

void native_ov007_021d8848(void) {
    func_02046150(0, 0, 5);
    func_020462e0(0, 2, 1);
    data_ov007_021da9d8[0] = func_02084924(7, 0, 2, 32, 2, 2, 3, 0, 1, 1);
    func_02085270((char *)data_ov007_021da9d8[0] + 60, 8, 0);
    ((u32 *)data_ov007_021da9d8[0])[32] |= 0x800;
}
