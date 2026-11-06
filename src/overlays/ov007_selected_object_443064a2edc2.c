typedef unsigned int u32;
typedef unsigned char u8;
typedef signed int s32;
typedef struct { u32 first; u32 second; u32 index; u32 prior; } Choice;
typedef struct { u32 words[36]; } Object;

extern volatile u32 data_ov007_021da9dc[];
extern u32 data_02101ae8[];
extern void func_0204861c(u32, u32);
extern void func_0202a51c(u32);
extern void func_020485b4(u32);
extern void func_020484dc(u32, u32);
extern u32 func_ov007_021d873c(u32);
extern void func_02048a44(void *, u32);
extern void func_020485c8(u32, void *);
extern u32 func_ov007_021d8634(u32);
extern u32 func_ov007_021d864c(u32);
extern void func_02048a60(void *, u32, u32);
extern void func_02048a9c(void *, u32);
extern void func_02048a94(void *, u32);
extern void func_ov007_021d91f4(void);
extern void func_ov007_021d8d48(void);
extern Choice func_ov007_021d85e4(void);
extern void func_02048644(void *, u32, u32);
extern void func_ov007_021d9138(void);
extern u32 func_ov007_021d8664(u32);
extern u32 func_ov007_021d8828(u32);
extern u32 func_020c20e4(u32);

void native_ov007_021d8e4c(void) {
    Choice choice = func_ov007_021d85e4();
    func_020485c8(1, (void *)data_ov007_021da9dc[2]);
    func_02048644((void *)data_ov007_021da9dc[2], data_ov007_021da9dc[4], 4);
    func_02048a60((void *)data_ov007_021da9dc[2], choice.first - 4, choice.second - 4);
    { u32 *object = (u32 *)data_ov007_021da9dc[2];
    object[31] = object[31] | 2; }
    func_02048a9c((void *)data_ov007_021da9dc[2], 0);
    func_02048a94((void *)data_ov007_021da9dc[2], 0);
}
