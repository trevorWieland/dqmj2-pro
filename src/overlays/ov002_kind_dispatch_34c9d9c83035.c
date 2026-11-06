typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;

extern u32 data_ov002_021db218[];
extern u32 data_ov002_021db218_alias1[];
extern u32 data_ov002_021db228[];
extern u32 data_ov002_021db28c[];
extern u8 data_ov002_021db280[];
extern u32 data_ov002_021daee4[];
extern u8 data_ov002_021daf9c[];
extern void func_ov002_021d88ac(void);
extern void func_ov002_021d874c(void);
extern u32 func_ov002_021d89ac(void);
extern void func_02041538(u32, u32, u32);
extern void func_02041510(u32, u32, u32);
extern void func_0205f9e4(u32 *);
extern u32 func_020644c0(void);
extern void func_ov002_021d8348(u32);
extern void func_ov002_021d7af8(u32, u32, u32, u32, u32, u32);
extern void func_0205fa4c(u32 *, u32);
extern void func_ov002_021d7630(u32);
extern void func_0205e814(u32, u32, u32);
extern u32 *func_ov002_021da040(void);
extern void func_ov002_021d7778(u32 *);
extern void func_ov002_021d838c(u32 *);
extern u16 *func_0202a634(void);
extern void func_0205e7a8(s32, u32);
extern void func_02064488(u32);
extern void func_ov002_021d8970(u32);
extern void func_ov002_021d7bb8(u32 *);
extern void func_ov002_021d75e4(void);
extern void func_ov002_021d81c8(u32);
extern void func_ov002_021d8ce0(u32);
extern void func_ov002_021d9084(u32);
extern u32 func_ov002_021d9830(u32, u32);
extern void func_ov002_021d9420(u32);
extern u32 func_ov002_021d9990(void);
extern u32 func_02027400(void);
extern void func_ov002_021d99c8(void);
extern void func_02049008(u32, s32, s32, s32, u32);
extern u32 *func_02049ad0(s32);
extern s32 func_ov002_021d7850(s32);
extern u32 func_02048f5c(u32);
extern u32 func_02048f6c(u32);
extern void func_02045dc4(u32, u32, u32, u32, u32, u32);
extern void func_02049f4c(u32 *);
extern void func_0206006c(u8 *, s32, s32, s32, s32);
extern void func_020851d4(void);
extern void func_02085200(void);

u32 native_ov002_021d9830(u32 kind, u32 value) {
    switch (kind) {
    case 0:
        func_ov002_021d7af8(21, 1, 5, 1, 1, 87);
        break;
    case 1:
        func_ov002_021d7af8(21, 1, 6, 1, 1, 87);
        break;
    case 2:
        func_ov002_021d7af8(21, 1, 7, 1, 1, 87);
        break;
    case 3:
        func_ov002_021d7af8(21, 1, 8, 1, 1, 87);
        break;
    case 4:
        func_ov002_021d7af8(21, 1, 9, 1, 1, 87);
        break;
    case 5:
        func_ov002_021d7bb8(func_ov002_021da040());
        func_ov002_021d7af8(21, 4, value, 1, 1, 87);
        break;
    case 6:
        func_ov002_021d7bb8(func_ov002_021da040());
        func_ov002_021d7af8(21, 5, value, 1, 1, 87);
        break;
    default:
        return 0;
    }
    func_ov002_021d7630(0);
    return 1;
}
