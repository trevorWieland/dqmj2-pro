typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u16 data_ov002_021db280[];
extern u8 data_ov002_021da4a0[];
extern u8 data_ov002_021da4ca[];
extern u32 *func_ov002_021da040(void);
extern void func_02048fcc(u32 *);
extern void func_ov002_021d7f98(u32 *, u32, u32, u32, u32, u32, u32);
extern void func_ov002_021d7dc4(u32 *, u32, u32, u16, u32, u32, u32, u32, u32, u32);
extern void func_ov002_021d7630(u32);
extern void func_ov002_021d8504(u32);
extern void func_ov002_021d76a8(u32, u32, u32);
extern void func_ov002_021d7c90(u32, u32, u32);
extern u32 *func_02049ad0(s8);
extern void func_02049ffc(u32);
extern void func_02086ad8(u32);
extern void func_0204a574(s8, u16 *, u32, u32, u32, u32, u32);
extern void func_ov002_021d8094(void);
extern u32 func_02048f5c(u32);
extern void func_02045dc4(u32, u32, u32, u32, u32, u32);
extern void func_ov002_021d811c(u32, u32, u32);
extern void func_ov002_021d7668(u32, u32);

void native_ov002_021d8ce0(u32 kind) {
    u32 *target = func_ov002_021da040();
    func_02048fcc(target);
    switch (kind) {
    case 0:
        func_ov002_021d7f98(target, 7, 6, 2, 5, 23, data_ov002_021db280[2]);
        target[1] = data_ov002_021db280[2] / 6 * 6;
        func_ov002_021d7630(1);
        func_ov002_021d8504(1);
        func_ov002_021d76a8(0, 200, 40);
        func_ov002_021d76a8(1, 200, 128);
        return;
    case 1:
        func_ov002_021d7dc4(target, 21, 2, data_ov002_021db280[2], 16, 1, 3, 30, 2, 0);
        func_ov002_021d7f98(target, data_ov002_021da4a0[data_ov002_021db280[2] * 6], 6, 2, 6, 23, data_ov002_021db280[3]);
        target[1] = data_ov002_021db280[3] / 6 * 6;
        func_ov002_021d7630(1);
        func_ov002_021d8504(1);
        func_ov002_021d76a8(0, 200, 48);
        func_ov002_021d76a8(1, 200, 136);
        return;
    case 2:
        func_ov002_021d7c90(21, 0, 4);
        func_ov002_021d7dc4(target, 21, 3, 239, 16, 1, 3, 30, 2, 0);
        func_ov002_021d7f98(target, 9, 6, 2, 6, 23, data_ov002_021db280[4]);
        target[1] = data_ov002_021db280[4] / 6 * 6;
        func_ov002_021d7630(1);
        func_ov002_021d8504(0);
        func_ov002_021d76a8(0, 200, 48);
        func_ov002_021d76a8(1, 200, 136);
        return;
    case 3:
        func_ov002_021d7c90(21, 0, 4);
        func_ov002_021d7dc4(target, 21, 3, 239, 16, 1, 3, 30, 2, 0);
        func_ov002_021d7dc4(target, 21, 2, data_ov002_021db280[4] + 7, 16, 2, 5, 29, 2, 1);
        func_ov002_021d7f98(target, data_ov002_021da4ca[data_ov002_021db280[4] * 6], 6, 2, 8, 23, data_ov002_021db280[5]);
        target[1] = data_ov002_021db280[5] / 6 * 6;
        func_ov002_021d7630(1);
        func_ov002_021d8504(0);
        func_ov002_021d76a8(0, 200, 64);
        func_ov002_021d76a8(1, 200, 152);
        break;
    }
}
