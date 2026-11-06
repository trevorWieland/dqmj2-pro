typedef unsigned int u32;
typedef unsigned char u8;
typedef signed char s8;
typedef signed int s32;
typedef struct { u32 words[36]; } Object;

extern u32 data_ov007_021da9dc[];
extern s8 data_ov007_021da924;
extern char data_ov007_021da928[];
extern char data_ov007_021da944[];
extern char data_ov007_021da960[];
extern void func_020485c8(u32, void *);
extern void func_02048644(void *, u32, u32);
extern void func_02048a9c(void *, u32);
extern void func_02048a94(void *, u32);
extern void func_02048a60(void *, u32, u32);
extern void func_ov007_021d93ac(u32, u32);
extern void func_0204861c(u32, u32);
extern void func_0202a51c(u32);
extern void func_020485b4(u32);
extern void func_020484dc(u32, u32);
extern void func_0201d444(char *, const char *, ...);
extern u32 func_0203cc2c(char *, u32);
extern u32 func_02040d18(u32, char *);
extern u32 func_02040d5c(u32, char *);
extern void func_02045a60(u32, u32, u32, u32);
extern void func_02045490(u32, u32, u32, u32);
extern void func_0202a498(u32, u32);

void native_ov007_021d8fbc(u32 kind) {
    u32 *object;
    u32 resource;
    if (kind == 0) {
        object = (u32 *)data_ov007_021da9dc[1];
        resource = data_ov007_021da9dc[8];
    } else {
        object = (u32 *)data_ov007_021da9dc[10];
        resource = data_ov007_021da9dc[4];
    }
    func_020485c8((u8)kind, object);
    func_02048644(object, resource, 18);
    object[31] = object[31] & ~2;
    func_02048a9c(object, 0);
    func_02048a94(object, 1);
    object[31] = object[31] | 12;
    func_ov007_021d93ac(kind, 0);
}

void native_ov007_021d9424(void) {
    s32 index;
    s32 other;
    if (data_ov007_021da9dc[3]) {
        for (index = 0; index < 16; index++) {
            func_0204861c(1, ((u8 *)&((Object *)data_ov007_021da9dc[3])[index])[129]);
        }
        func_0202a51c(data_ov007_021da9dc[3]);
    }
    if (data_ov007_021da9dc[2]) {
        func_0204861c(1, ((u8 *)data_ov007_021da9dc[2])[129]);
        func_0202a51c(data_ov007_021da9dc[2]);
    }
    if (data_ov007_021da9dc[6]) {
        for (other = 0; other < 3; other++) {
            func_0204861c(1, ((u8 *)&((Object *)data_ov007_021da9dc[6])[other])[129]);
        }
        func_0202a51c(data_ov007_021da9dc[6]);
    }
    if (data_ov007_021da9dc[10]) {
        func_0204861c(1, ((u8 *)data_ov007_021da9dc[10])[129]);
        func_0202a51c(data_ov007_021da9dc[10]);
    }
    if (data_ov007_021da9dc[5]) {
        func_020485b4(data_ov007_021da9dc[5]);
    }
    func_020484dc(1, ((u8 *)data_ov007_021da9dc)[1]);
}

void native_ov007_021d9770(void) {
    char graphics[32];
    char palette[32];
    char path[32];
    s32 number = data_ov007_021da924 == 9 ? 8 : data_ov007_021da924 + 1;
    u32 bank;
    u32 graphicsData;
    u32 graphicsSize;
    u32 paletteData;
    u32 paletteSize;
    func_0201d444(path, data_ov007_021da928, number);
    func_0201d444(graphics, data_ov007_021da944, number);
    func_0201d444(palette, data_ov007_021da960, number);
    bank = func_0203cc2c(path, 5);
    if (bank != 0) {
        graphicsData = func_02040d18(bank, graphics);
        graphicsSize = func_02040d5c(bank, graphics);
        paletteData = func_02040d18(bank, palette);
        paletteSize = func_02040d5c(bank, palette);
        func_02045a60(1, paletteData, 0, paletteSize);
        func_02045490(1, graphicsData, 0, graphicsSize);
    }
    func_0202a498(5, bank);
}
