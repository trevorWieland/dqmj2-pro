typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef short s16;
typedef unsigned int u32;
typedef int s32;

extern u8 data_ov002_021da560[];
extern u32 data_ov002_021db098[];
extern u8 data_ov002_021da5bc[];
extern u8 data_ov002_021daef8[];
extern u8 data_021c9698[];
extern u32 data_ov002_021db2a4[];
extern u8 data_ov002_021db2b8[];
extern u32 data_ov002_021db2c8[];

typedef struct {
    s8 a;
    s8 b;
    s8 c;
    u8 pad;
    s32 count;
    u32 value8;
    u32 value12;
    u32 value16;
} State;

typedef struct {
    u32 value0;
    u32 value4;
    u32 value8;
    u16 value12;
    u16 value14;
} Object;

extern State data_ov002_021daee4;
extern void func_ov002_021d7630(u32);
extern void func_ov002_021d76f0(u32);
extern void func_ov002_021d7744(u32, u32);
extern void func_ov002_021d7668(u32, u32);
extern u32 func_02065730(u32 *, s32, u32, u32, u32);
extern void func_02049008(Object *, u32, s8, s8, s8);
extern u32 func_02049f24(void);
extern void func_02049f30(void);
extern u32 *func_02049ad0(s32);
extern void func_02046af4(u8 *, u32, u32, u32, u32, u32);
extern void func_02049f14(u32);
extern void func_ov002_021d7998(u32, s32, u32, u32, u32, u32, u32, u32, u32);
extern void func_ov002_021d7ab0(u32, u32, u32, u32, s16);
extern void func_02049f4c(u32 *);
extern void func_02049ffc(u32);
extern void func_0201d444(void *, u8 *);
extern u32 func_0203cc2c(void *, u32);
extern void func_0204820c(u32, u32, u32);
extern void func_0202a498(u32, u32);
extern void func_02048308(void);
extern u32 *func_ov002_021da04c(void);
extern void func_ov002_021d828c(s32);
extern u32 func_02048f7c(u32);
extern void func_02045680(u32);
extern u32 func_0202a1e0(u32);
extern void func_02048e74(u8 *, u32);
extern void func_02048fcc(u32 *);
extern void func_ov002_021d9ca4(void);
extern void func_ov002_021d9ea8(void);
extern u32 func_02027400(void);

void native_ov002_021d75e4(void) {
    s8 index;
    func_ov002_021d7630(0);
    func_ov002_021d76f0(0);
    func_ov002_021d7744(160, 8);
    index = 0;
    do {
        func_ov002_021d7668(index, 0);
        index++;
    } while (index < 2);
}

void native_ov002_021d7930(u32 *values) {
    s32 index = 0;
    u8 *entry = data_ov002_021da560;
    u32 *target = data_ov002_021db098;
    do {
        u32 slot = entry[2];
        values[slot] += func_02065730(target, (s8)entry[0], entry[1], slot, values[slot]);
        index++;
        entry += 3;
        target += 3;
    } while (index < 9);
}

void native_ov002_021d7a50(Object *target, u32 first, u32 second, u32 third, s8 fourth, s8 fifth, s8 sixth, u32 seventh) {
    target->value14 = first;
    target->value12 = second;
    target->value0 = seventh;
    target->value4 = 0;
    func_02049008(target, third, fourth, fifth, sixth);
    data_ov002_021daee4.a = third;
    data_ov002_021daee4.b = fourth;
    data_ov002_021daee4.c = fifth;
}

void native_ov002_021d7bb8(u32 *values) {
    u32 old = func_02049f24();
    u32 *object;
    u8 *nested;
    func_02049f30();
    object = func_02049ad0((s8)(values[0] - values[1] + 5));
    nested = (u8 *)((u32 *)object[0])[1];
    func_02046af4(data_021c9698, ((u32 *)nested)[26], nested[94], 0, old, 255);
    func_02049f14(old);
}

void native_ov002_021d7c28(u8 *target, u32 first, u32 second, u32 third) {
    func_ov002_021d7998(0, (s8)target[16], 127, 1, 1, 20, 2, 1, 1);
    func_ov002_021d7ab0(0, first, second, third, 8);
}

void native_ov002_021d7c90(u32 first, u32 second, u32 third) {
    u32 *object = func_02049ad0(0);
    u32 *nested;
    func_02049f4c(object);
    func_02049ffc(((u32 *)object[0])[1]);
    func_ov002_021d7ab0(0, first, second, third, 8);
    nested = (u32 *)((u32 *)object[0])[1];
    nested[6] |= 2;
}

void native_ov002_021d8094(void) {
    u8 buffer[32];
    u32 value;
    func_0201d444(buffer, data_ov002_021da5bc);
    value = func_0203cc2c(buffer, 2);
    func_0204820c(value, 256, 64);
    func_0202a498(2, value);
    func_02048308();
    data_ov002_021daee4.value12 = 1020;
}

void native_ov002_021d9af0(void) {
    u32 old = func_0202a1e0(2);
    func_02048e74(data_ov002_021db2b8, 0);
    func_02048fcc(data_ov002_021db2c8);
    data_ov002_021db2a4[8] = 4;
    func_ov002_021d9ca4();
    func_ov002_021d9ea8();
    if (func_02027400() == 15) {
        data_ov002_021db2a4[5] = 2;
    } else {
        data_ov002_021db2a4[5] = 0;
    }
    func_0202a1e0(old);
}
