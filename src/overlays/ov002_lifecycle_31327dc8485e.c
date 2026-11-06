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

void native_ov002_021d750c(void) {
    if (data_ov002_021daec0[3] != 0) {
        func_0204861c(1, ((u8 *)data_ov002_021daec0[3])[129]);
        func_0202a498(2, data_ov002_021daec0[3]);
        data_ov002_021daec0[3] = 0;
    }
    if (data_ov002_021daec0[7] != 0) {
        func_020485b4(data_ov002_021daec0[7]);
    }
    if (data_ov002_021daec0[5] != 0) {
        func_0205f920(data_ov002_021daec0[5], 1, 2);
        func_0202a498(2, data_ov002_021daec0[5]);
        data_ov002_021daec0[5] = 0;
    }
    if (data_ov002_021daec0[4] != 0) {
        func_0205f920(data_ov002_021daec0[4], 1, 2);
        func_0202a498(2, data_ov002_021daec0[4]);
        data_ov002_021daec0[4] = 0;
    }
    func_020484dc(1, ((u8 *)data_ov002_021daec0)[0]);
}

void native_ov002_021d88ac(void) {
    u32 *target;
    u32 output;
    func_ov002_021d7c28(func_ov002_021da040(), 21, 0, 0);
    target = func_ov002_021da040();
    func_ov002_021d7e64(target, 3, data_ov002_021da498, 2, 5, 28, func_ov002_021da040()[0]);
    func_ov002_021d7630(1);
    func_ov002_021d8504(1);
    func_0204b85c(data_ov002_021db228, &output, 8, 1, 0, 51, 0);
    func_02048a60(func_0205f98c(data_ov002_021db228[7], 0), 224, 96);
    func_0205fa4c(data_ov002_021db228, 0);
    func_ov002_021da2e0();
}

u32 native_ov002_021d99e0(void) {
    u8 buffer[32];
    u32 count = 8;
    u8 *cursor = buffer;
    do {
        cursor[0] = 0;
        cursor[1] = 0;
        cursor[2] = 0;
        cursor[3] = 0;
        cursor += 4;
    } while (--count != 0);
    func_0205db90(buffer, data_ov002_021da5d4, ~0U);
    data_ov002_021db29c[1] = func_0205d9e8(1, buffer, data_ov002_021da478, data_ov002_021da46c, 6);
    func_0205db90(buffer, data_ov002_021da5e0, ~0U);
    data_ov002_021db29c[0] = func_0205d9e8(1, buffer, data_020dc368, data_020dc348, 16);
    func_0205df8c(data_ov002_021db29c[0]);
    return 1;
}

u32 native_ov002_021da1c4(void) {
    u32 *output = data_ov002_021db3bc;
    u32 result = 13;
    switch (data_ov002_021db3b8[2]) {
    case 0:
        if (func_02064510() != 0) {
            output[1] = 1;
        }
        break;
    case 1:
        func_ov002_021da450();
        func_02061238(1, 2, 0);
        func_020406a8(1);
        func_020612ec(40, 1, 0x8000, 0);
        func_0206157c();
        func_020273d8(10);
        output[1] = 2;
        break;
    case 2:
        if (data_ov002_021db3b8[3] != 13) {
            output[1] = 3;
        }
        func_0206157c();
        break;
    case 3:
        func_020c1898(1);
        result = data_ov002_021db3b8[3];
        func_0206157c();
        break;
    }
    return result;
}
