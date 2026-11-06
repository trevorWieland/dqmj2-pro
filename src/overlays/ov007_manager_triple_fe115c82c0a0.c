typedef unsigned int u32;
typedef unsigned char u8;
typedef signed char s8;
typedef signed int s32;
typedef struct { u32 words[36]; } Object;

extern volatile u32 data_ov007_021da9dc[];
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

void native_ov007_021d8ee8(void) {
    s32 index;
    for (index = 0; index < 3; index++) {
        func_020485c8(1, &((Object *)data_ov007_021da9dc[6])[index]);
        func_02048644(&((Object *)data_ov007_021da9dc[6])[index], data_ov007_021da9dc[4], 5);
        {Object *object = &((Object *)data_ov007_021da9dc[6])[index]; object->words[31] = object->words[31] & ~2;}
        func_02048a9c(&((Object *)data_ov007_021da9dc[6])[index], 0);
        func_02048a94(&((Object *)data_ov007_021da9dc[6])[index], 2);
    }
    func_02048a60((void *)data_ov007_021da9dc[6], 128, 40);
    func_02048a60((u8 *)data_ov007_021da9dc[6] + 144, 90, 60);
    func_02048a60((u8 *)data_ov007_021da9dc[6] + 288, 110, 50);
}
