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

u32 native_ov002_021d85c4(void) {
    u32 *state = data_ov002_021db218_alias1;
    u32 result = 0;
    switch (data_ov002_021db218[1]) {
    case 0:
        func_ov002_021d88ac();
        state[1] = 1;
        break;
    case 1:
        func_ov002_021d874c();
        break;
    case 2:
        if (func_ov002_021d89ac() != 0) {
            state[1] = 1;
        }
        break;
    case 3:
        func_02041538(1, 2, 10);
        result = 1;
        break;
    case 4:
        result = 2;
        break;
    case 5:
        func_0205f9e4(data_ov002_021db228);
        if (func_020644c0() != 0) {
            func_ov002_021d8348(0);
            func_ov002_021d7af8(5, 6, 9, 0, 0, 87);
            func_0205fa4c(data_ov002_021db228, 0);
            state[1] = 6;
        }
        break;
    case 6:
        if (func_ov002_021d89ac() != 0) {
            func_ov002_021d7630(1);
            state[1] = 7;
        }
        break;
    case 7:
        func_02041510(1, 2, 10);
        func_02041538(1, 2, 10);
        func_0205e814(0, 0, 10);
        result = 3;
        break;
    }
    func_ov002_021d7778(func_ov002_021da040());
    func_ov002_021d838c(func_ov002_021da040());
    return result;
}
