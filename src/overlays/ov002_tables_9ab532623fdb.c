typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef int s32;

extern u8 data_ov002_021da540[];
extern u8 data_ov002_021da544[];
extern u32 data_ov002_021daec0[];
extern u32 data_02101ae8[];
extern u8 data_ov002_021da57b[];
extern u32 data_ov002_021daf9c[];
extern u8 data_ov002_021daef8[];
extern u8 data_ov002_021dafa7[];
extern u32 data_ov002_021daf18[];
extern u8 data_ov002_021daf1c[];
extern u32 data_ov002_021db2a4[];
extern u8 data_ov002_021db28c[];
extern u8 data_ov002_021db284[];
extern u8 data_ov002_021db280[];
extern u32 data_ov002_021db270[];
extern u32 data_ov002_021db270_alias1[];
extern u8 data_ov002_021db218[];
extern u8 data_ov002_021db228[];
extern s8 data_ov002_021db3b8[];
extern u8 data_ov002_021db3bc[];

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
extern State data_ov002_021daee4;

extern void func_02049130(u32, u32, u32);
extern void func_0205f9e4(u32);
extern u32 func_02048f5c(u32);
extern u32 func_02048f6c(u32);
extern s32 func_0205ffcc(u32 *, s32, u32, u32, s32);
extern u32 *func_02049ad0(s32);
extern void func_02049be4(u32 *, u32, s32, s32, u32, u8, u8, u8, u32, s8, u32);
extern void func_ov002_021d7998(s32, s32, u32, u32, u8, u8, u8, s8, u32);
extern void func_ov002_021d7ab0(s32, u32, u32, u32, short);
extern s32 func_ov002_021d7850(s32);
extern void func_02045dc4(u32, u32, u32, u32, u32, u32);
extern void func_0205ff4c(u32);
extern u32 func_ov002_021d80f0(u32, u32);
extern void func_02045490(u32, u8 *, u32, u32);
extern void func_02045770(u32, u32, u32, u32, u32, u32, u32, u32, u8 *);
extern void func_0204518c(u32 *, u32, u32);
extern u32 func_0202a44c(u32, u32, u32);
extern void func_02008e0c(u32, u32, u32);
extern void func_02045994(u32, u32, u32, u32);
extern void func_02048e74(u8 *, u32);
extern void func_02008d78(void *, u32, u32);
extern u32 *func_ov002_021da040(void);
extern u32 func_ov002_021da030(void);
extern void func_ov002_021d7c28(u32 *, u32, u32, u32);
extern u32 func_02027400(void);
extern void func_020414c8(u32);
extern void func_02041510(u32, u32, u32);
extern void func_02041538(u32, u32, u32);
extern void func_ov002_021d8ab8(void);
extern void func_0207f254(void);
extern u32 func_0207e874(void);
extern u32 func_0207f390(void);
extern void func_ov002_021d8b00(void);
extern u32 func_02041814(void);
extern void func_0202a090(u32, u32);
extern u32 func_0202a1e0(u32);
extern void func_ov002_021d99e0(void);
extern void func_ov002_021da2f0(void);
extern void func_0205e644(void);
extern void func_0205e66c(void);
extern void func_0205e73c(u32);
extern void func_0205e7a8(u32, u32);
extern void func_020644f4(u32);

void native_ov002_021d789c(s32 *values) {
    u8 *entry;
    u32 *target;
    u32 slot = func_02048f5c(1);
    s8 index;
    entry = data_ov002_021da57b;
    target = data_ov002_021daf9c;
    index = 0;
    do {
        values[slot] += func_0205ffcc(target, (s8)entry[0], entry[1], slot, values[slot]);
        index++;
        entry += 3;
        target += 3;
    } while (index < 21);
    data_ov002_021daee4.value16 = values[func_02048f6c(1)] >> 5;
}

void native_ov002_021d7998(s32 index, s32 first, s32 second, u32 third, u8 fourth, u8 fifth, u8 sixth, s8 seventh, u32 eighth) {
    u32 *object = func_02049ad0(index);
    u32 *nested;
    s32 count;
    func_02049be4(object, 1, first, second, third, fourth, fifth, sixth, data_ov002_021daee4.value16, seventh, eighth);
    nested = (u32 *)((u32 *)object[0])[1];
    nested[6] |= 2;
    data_ov002_021daee4.value16 += fifth * sixth;
    count = data_ov002_021daee4.count++;
    data_ov002_021daef8[count] = index;
}

void native_ov002_021d811c(u32 count, u32 first, u32 second) {
    u32 slot = func_02048f6c(1);
    func_ov002_021d80f0((u32)data_ov002_021daf18, count);
    func_02045490(slot, data_ov002_021daf1c, data_ov002_021daee4.value12 << 5, 128);
    func_02045770(1, slot, 2, 2, first, second, 32, data_ov002_021daee4.value12, (u8 *)data_ov002_021daf18[0] + 8);
    data_ov002_021daee4.value12 -= 4;
}

void native_ov002_021d8b24(void) {
    func_02048e74(data_ov002_021db28c, 0);
    func_02008d78(data_ov002_021db284, 0, 8);
    func_ov002_021d7c28(func_ov002_021da040(), 21, 0, 4);
    if (func_02027400() == 15) {
        func_020414c8(63);
        func_02041510(0, 2, 10);
        func_02041538(0, 2, 10);
    }
    data_ov002_021db280[0] = 0;
}

void native_ov002_021d8514(void) {
    func_02048e74(data_ov002_021db218, 0);
    func_02008d78(data_ov002_021db228, 0, 72);
    switch (func_ov002_021da030()) {
    case 1:
        func_02041538(0, 2, 10);
        func_ov002_021da040()[0] = 0;
        break;
    case 2:
        func_ov002_021da040()[0] = 1;
        break;
    case 4:
        func_020414c8(63);
        func_02041510(0, 2, 10);
        func_02041538(0, 2, 10);
        func_ov002_021da040()[0] = 0;
        break;
    }
}
