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
extern void func_ov002_021d7998(s8, s32, u32, u32, u32, u32, u32, u32, u32);
extern void func_ov002_021d7ab0(s8, u32, u32, u32, u32);
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

void native_ov002_021d7e64(u8 *target, u32 count, u16 *labels, u32 mode, u8 first, u32 second, u32 third) {
    u8 index;
    u8 base = first;

    func_ov002_021d7998(4, (s8)target[16], 12, (u8)(mode - 1), (u8)(base - 1), (u8)(second + 2), (u8)(count * 2 + 2), 1, 0);
    index = 0;
    if (index < count) do {
        s32 slot = index + 5;
        func_ov002_021d7998(slot, (s8)target[16], 1, mode, (u8)(base + index * 2), second, 2, 0, 1);
        if (labels != 0) {
            func_ov002_021d7ab0(slot, 21, 0, labels[index], 16);
        }
        index++;
    } while (index < count);
    func_ov002_021d7a50(target, count, count, 5, 0, 1, 2, third);
}
