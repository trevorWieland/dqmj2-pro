typedef unsigned char u8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u8 data_ov002_021da5c8[];
extern u8 data_ov002_021db228[];
extern u8 data_ov002_021db270[];
extern u8 data_ov002_021db29c[];
extern u8 data_020dc368[];
extern u8 data_020dc348[];
extern u8 data_ov002_021db2a0[];
extern u32 data_ov002_021db2a4[];
extern u32 data_ov002_021db2c8[];
extern u32 data_ov002_021db2a8[];
extern signed char data_ov002_021db3b8[];
extern u8 data_ov002_021db3cc[];

extern u32 *func_02049ad0(u32);
extern void func_02049f4c(u32 *);
extern void func_0204a04c(u32, u32, u32, u32);
extern void func_02085270(u32 *, s16, u32);
extern u32 func_0202a818(u8 *, u32, u32, u32);
extern u32 *func_ov002_021da04c(void);
extern void func_02049b84(u32);
extern void func_020414c8(u32);
extern void func_ov002_021d7630(u32);
extern u32 func_02048f7c(u32);
extern void func_0205f920(u8 *, u32, u32);
extern void func_ov002_021d75e4(void);
extern void func_ov002_021d81c8(u32);
extern u32 *func_ov002_021da040(void);
extern void func_ov002_021d7bb8(u32 *);
extern void func_ov002_021d7af8(u32, u32, u32, u32, u32, u32);
extern u16 *func_0202a634(void);
extern void func_ov002_021d8348(u32);
extern void func_02048e74(u8 *, u32);
extern void func_ov002_021d9c90(void);
extern void func_0207e97c(void);
extern void func_0207e948(void);
extern void func_ov002_021da100(void);
extern void func_02008d78(void *, u32, u32);
extern u32 func_02063aa4(void);
extern void func_0207e720(void *);
extern u32 func_0207f3b0(void);
extern void func_02008e0c(u32, u32, u32);
extern void func_ov002_021d7778(u32 *);
extern void func_ov002_021d838c(u32 *);
extern void func_0205dbf0(u32, u8 *, u8 *, u8 *, u32);
extern void func_0205df8c(u32);
extern void func_0205dbc4(u32, u8 *);
extern void func_ov002_021d7844(void);
extern void func_ov002_021d750c(void);
extern void func_ov002_021d9e70(void);
extern void func_02049940(u32);
extern void func_020848d4(u32);
extern void func_0204617c(u32, u32);
extern u32 func_0202a1e0(u32);
extern void func_ov002_021d9ca4(void);
extern void func_ov002_021d9ea8(void);
extern void func_02062328(void);
extern void func_020d253c(void);
extern void func_02061898(void);
extern void func_020406a8(u32);
extern void func_ov002_021da434(void);
extern u32 func_ov002_021d9aa4(void);
extern void func_0202a164(u32);
extern void func_ov002_021da450(void);
extern void func_020d3428(void);
extern void func_020bee08(u8 *);
extern void func_020d23cc(u8 *);

void native_ov002_021d7ab0(u32 first, u32 second, u32 third, u32 fourth, s16 fifth) {
    u32 *object = func_02049ad0(first);
    u32 nested = ((u32 *)object[0])[1];
    func_02049f4c(object);
    func_0204a04c(nested, second, third, fourth);
    func_02085270((u32 *)(nested + 60), fifth, 0);
}

u32 native_ov002_021d80f0(u32 first, u32 count) {
    return func_0202a818(data_ov002_021da5c8, first, 132, count * 132) != 0;
}

void native_ov002_021d8348(u32 flag) {
    u32 *values = func_ov002_021da04c();
    func_02049b84(flag);
    if (flag != 0) {
        func_020414c8(63);
    }
    func_ov002_021d7630(1);
    values[func_02048f7c(1)] = 32;
}

void native_ov002_021d8724(void) {
    func_0205f920(data_ov002_021db228, 1, 2);
    func_ov002_021d75e4();
    func_ov002_021d81c8(1);
}

void native_ov002_021d8970(u32 value) {
    func_ov002_021d7bb8(func_ov002_021da040());
    func_ov002_021d7af8(21, 1, value, 1, 1, 87);
}

u32 native_ov002_021d89ac(void) {
    if ((func_0202a634()[1] & 0xff7) == 0) {
        return 0;
    }
    func_ov002_021d8348(1);
    return 1;
}

void native_ov002_021d89dc(void) {
    func_02048e74(data_ov002_021db270, 0);
    func_ov002_021d9c90();
    func_0207e97c();
}

void native_ov002_021d8aa8(void) {
    func_0207e948();
    func_ov002_021da100();
}

void native_ov002_021d8ab8(void) {
    struct {
        u8 a;
        u8 padding[7];
        u32 value;
        u8 b;
        u8 c;
        u8 tail[2];
    } item;
    func_02008d78(&item, 0, 16);
    item.a = 0;
    item.value = func_02063aa4();
    item.b = 16;
    item.c = 1;
    func_0207e720(&item);
}

void native_ov002_021d8b00(void) {
    u32 target = func_0207f3b0();
    func_02008e0c(target, func_02063aa4(), 20);
}

void native_ov002_021d8ccc(void) {
    func_ov002_021d75e4();
    func_ov002_021d81c8(1);
}

u32 native_ov002_021d9990(void) {
    u16 *keys = func_0202a634();
    func_ov002_021da040();
    if ((keys[1] & 0xff7) == 0) {
        return 0;
    }
    func_ov002_021d8348(1);
    return 1;
}

void native_ov002_021d99c8(void) {
    func_ov002_021d7778(func_ov002_021da040());
    func_ov002_021d838c(func_ov002_021da040());
}

u32 native_ov002_021d9aa4(void) {
    func_0205dbf0(1, data_ov002_021db29c, data_020dc368, data_020dc348, 16);
    func_0205df8c(0);
    func_0205dbc4(1, data_ov002_021db2a0);
    return 1;
}

void native_ov002_021d9c90(void) {
    func_ov002_021d7844();
    func_ov002_021d750c();
    func_ov002_021d9e70();
}

void native_ov002_021d9e70(void) {
    func_02049940(1);
    func_020848d4(1);
    func_020848d4(2);
    func_0204617c(1, 2);
    func_0204617c(2, 2);
}

u32 native_ov002_021da030(void) {
    return data_ov002_021db2a4[8];
}

void native_ov002_021da100(void) {
    u32 old = func_0202a1e0(2);
    func_ov002_021d9ca4();
    func_0202a1e0(old);
    func_ov002_021d9ea8();
}

void native_ov002_021da28c(void) {
    func_02062328();
    func_020d253c();
    func_02061898();
    func_020406a8(0);
    func_ov002_021da434();
    func_ov002_021d9aa4();
    func_0202a1e0(data_ov002_021db3b8[0]);
    func_0202a164(2);
    func_0202a164(1);
}

void native_ov002_021da2d0(u32 value) {
    ((u32 *)data_ov002_021db3b8)[3] = value;
}

void native_ov002_021da2e0(void) {
    func_ov002_021da450();
    func_020d3428();
}

void native_ov002_021da434(void) {
    func_020848d4(0);
    func_0204617c(0, 2);
}

void native_ov002_021da450(void) {
    func_020bee08(data_ov002_021db3cc);
    func_020d23cc(data_ov002_021db3cc);
}
