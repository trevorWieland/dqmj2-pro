typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;

extern u8 data_ov007_021da0d4[];
extern u8 data_ov007_021da0dc[];
extern u8 data_020dae90[];
extern u8 data_020dae88[];
extern u32 data_ov007_021da980[];

extern void func_0205db90(void *, const void *, u32);
extern u32 func_0205d9e8(u32, void *, void *, void *, u32);
extern void func_ov007_021d963c(void);
extern void func_ov007_021d961c(u32);
extern void func_0202a090(u32, u32);
extern u32 func_0202a1e0(u32);
extern void func_ov007_021d740c(void);
extern void func_ov007_021d7240(void);
extern void func_ov007_021d7460(void);
extern void func_020273d8(u32);
extern void func_0201d444(void *, void *, u32);
extern u32 func_ov007_021d86dc(u32);
extern u32 func_ov007_021d870c(u32);
extern u32 func_ov007_021d86f4(u32);
extern u32 func_0203cc2c(void *, u32);
extern u32 func_02040d18(u32, u32);
extern u32 func_02040d5c(u32, u32);
extern void func_02007308(u32, u32);
extern void func_02005158(void);
extern void func_020051f8(u32, u32, u32);
extern void func_02005268(void);
extern void func_020459dc(u32, u32, u32, u32);
extern void func_0204540c(u32, u32, u32, u32);
extern void func_0202a498(u32, u32);
extern void func_ov007_021d8938(void);

void native_ov007_021d740c(void) {
    u8 name[32];
    func_0205db90(name, data_ov007_021da0d4, ~0U);
    data_ov007_021da980[12] = func_0205d9e8(5, name, data_020dae90, data_020dae88, 4);
}

void native_ov007_021d7460(void) {
    func_ov007_021d963c();
    func_ov007_021d961c(85);
    func_ov007_021d961c(82);
    func_ov007_021d961c(92);
    func_ov007_021d961c(170);
}

void native_ov007_021d748c(void) {
    func_0202a090(5, 0x108000);
    ((u8 *)data_ov007_021da980)[0] = func_0202a1e0(5);
    func_ov007_021d740c();
    func_ov007_021d7240();
    func_ov007_021d7460();
    data_ov007_021da980[13] = 0;
    data_ov007_021da980[11] = 0;
    data_ov007_021da980[1] = 0;
    data_ov007_021da980[10] = 0;
    data_ov007_021da980[4] = 0;
    func_020273d8(5);
}

u32 native_ov007_021d74e4(u32 index) {
    u8 name[32];
    u32 first;
    u32 second;
    u32 third;
    u32 result = 0;
    if (index >= 15) {
        return result;
    }
    func_0201d444(name, data_ov007_021da0dc, index + 1);
    first = func_ov007_021d86dc(index);
    second = func_ov007_021d870c(index);
    third = func_ov007_021d86f4(index);
    if (data_ov007_021da980[9] == 0) {
        data_ov007_021da980[9] = func_0203cc2c(name, 5);
        if (data_ov007_021da980[9] != 0) {
            data_ov007_021da980[2] = func_02040d18(data_ov007_021da980[9], first);
            data_ov007_021da980[3] = func_02040d5c(data_ov007_021da980[9], first);
            data_ov007_021da980[7] = func_02040d18(data_ov007_021da980[9], second);
            data_ov007_021da980[8] = func_02040d5c(data_ov007_021da980[9], second);
            data_ov007_021da980[6] = func_02040d18(data_ov007_021da980[9], third);
            data_ov007_021da980[5] = func_02040d5c(data_ov007_021da980[9], third);
            result = 1;
        }
    }
    return result;
}

void native_ov007_021d75f0(void) {
    func_02007308(data_ov007_021da980[6], data_ov007_021da980[5]);
    func_02005158();
    func_020051f8(data_ov007_021da980[6], 0, data_ov007_021da980[5]);
    func_02005268();
    func_020459dc(0, data_ov007_021da980[7], 0, data_ov007_021da980[8]);
    func_0204540c(0, data_ov007_021da980[2], 0, data_ov007_021da980[3]);
}

void native_ov007_021d7658(void) {
    data_ov007_021da980[7] = 0;
    data_ov007_021da980[2] = 0;
    data_ov007_021da980[6] = 0;
    func_0202a498(5, data_ov007_021da980[9]);
    data_ov007_021da980[9] = 0;
}

void native_ov007_021d7690(void) {
    void (*target)(void) = func_ov007_021d8938;
    target();
}

void native_ov007_021d769c(void) {
}
