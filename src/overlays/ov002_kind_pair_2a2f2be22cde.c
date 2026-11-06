typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;

extern u32 data_ov002_021daec0[];
extern u16 data_ov002_021da498[];
extern u32 data_ov002_021db228[];
extern u8 data_ov002_021da5d4[];
extern u8 data_ov002_021da5e0[];
extern u8 data_ov002_021da478[];
extern u8 data_ov002_021da46c[];
extern u8 data_020dc368[];
extern u8 data_020dc348[];
extern u32 data_ov002_021db29c[];
extern u32 data_ov002_021db3b8[];
extern u32 data_ov002_021db3bc[];
extern void func_0204861c(u32, u32);
extern void func_0202a498(u32, u32);
extern void func_020485b4(u32);
extern void func_0205f920(u32, u32, u32);
extern void func_020484dc(u32, u32);
extern void func_ov002_021d7998(s32, s32, u32, u32, u32, u32, u32, u32, u32);
extern void func_ov002_021d7ab0(s32, u32, u32, u32, u32);
extern u32 *func_02049ad0(s32);
extern void func_02085418(u32, u32);
extern void func_ov002_021d7a50(u8 *, u32, u32, u32, u32, u32, u32, u32);
extern u32 *func_ov002_021da040(void);
extern void func_ov002_021d7c28(u32 *, u32, u32, u32);
extern void func_ov002_021d7e64(u32 *, u32, u16 *, u32, u8, u32, u32);
extern void func_ov002_021d7630(u32);
extern void func_ov002_021d8504(u32);
extern void func_0204b85c(u32 *, void *, u32, u32, u32, u32, u32);
extern u32 func_0205f98c(u32, u32);
extern void func_02048a60(u32, u32, u32);
extern void func_0205fa4c(u32 *, u32);
extern void func_ov002_021da2e0(void);
extern void func_0205db90(void *, u8 *, u32);
extern u32 func_0205d9e8(u32, void *, u8 *, u8 *, u32);
extern void func_0205df8c(u32);
extern u32 func_02064510(void);
extern void func_ov002_021da450(void);
extern void func_02061238(u32, u32, u32);
extern void func_020406a8(u32);
extern void func_020612ec(u32, u32, u32, u32);
extern void func_0206157c(void);
extern void func_020273d8(u32);
extern void func_020c1898(u32);

void native_ov002_021d7cf0(u8 *target, u32 kind) {
    s32 index;
    u32 third;
    u32 fifth;
    switch (kind) {
    case 0:
        index = 29;
        func_ov002_021d7998(index, (s8)target[16], 3, 19, 1, 13, 2, 1, 1);
        third = 3;
        fifth = 16;
        break;
    case 1:
        index = 30;
        func_ov002_021d7998(index, (s8)target[16], 3, 22, 1, 10, 2, 1, 1);
        third = 4;
        fifth = 8;
        break;
    }
    func_ov002_021d7ab0(index, 5, 2, third, fifth);
    func_02085418(((u32 *)func_02049ad0(index)[0])[1], 3);
}
