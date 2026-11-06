typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;

extern u32 data_ov007_021da0f4[];
extern u32 func_ov007_021d873c(u32);
extern u32 func_ov007_021d8634(u32);
extern u32 func_ov007_021d864c(u32);
extern u32 func_ov007_021d867c(u32);
extern void func_ov007_021d7aa0(u32);
extern s32 func_ov007_021d7e1c(u32);
extern u16 *func_0202a634(void);
extern u32 func_ov007_021d8170(void);
extern void func_ov007_021d9628(u32);
extern s32 func_ov007_021d86ac(u32);
extern void func_0205be34(u32);
extern void func_0205bdfc(u32);
extern void func_020c20f4(u32);
extern void func_0205bf2c(u32);
extern u32 func_ov007_021d86c4(u32);
extern void func_0205c060(u32);
extern void func_020c211c(u32);
extern s32 func_ov007_021d876c(u32);
extern void func_0203d0d8(u32, u32);

u32 native_ov007_021d8170(void) {
    u32 flags = 0;
    if (func_ov007_021d7e1c(1) != -1) {
        flags |= 1;
    }
    if (func_ov007_021d7e1c(2) != -1) {
        flags |= 2;
    }
    if (func_ov007_021d7e1c(3) != -1) {
        flags |= 4;
    }
    if (func_ov007_021d7e1c(4) != -1) {
        flags |= 8;
    }
    return flags;
}

u32 native_ov007_021d81d0(void) {
    u16 *input = func_0202a634();
    u32 flags = func_ov007_021d8170();
    u32 prior = data_ov007_021da0f4[2];
    if ((input[0] & 64) && (flags & 1)) {
        data_ov007_021da0f4[2] = func_ov007_021d7e1c(1);
        data_ov007_021da0f4[3] = prior;
    } else if ((input[0] & 128) && (flags & 2)) {
        data_ov007_021da0f4[2] = func_ov007_021d7e1c(2);
        data_ov007_021da0f4[3] = prior;
    } else if ((input[0] & 32) && (flags & 4)) {
        data_ov007_021da0f4[2] = func_ov007_021d7e1c(3);
        data_ov007_021da0f4[3] = prior;
    } else if ((input[0] & 16) && (flags & 8)) {
        data_ov007_021da0f4[2] = func_ov007_021d7e1c(4);
        data_ov007_021da0f4[3] = prior;
    }
    if (prior == data_ov007_021da0f4[2]) {
        return 0;
    }
    data_ov007_021da0f4[0] = func_ov007_021d8634(data_ov007_021da0f4[2]);
    data_ov007_021da0f4[1] = func_ov007_021d864c(data_ov007_021da0f4[2]);
    func_ov007_021d7aa0(func_ov007_021d867c(data_ov007_021da0f4[2]));
    func_ov007_021d9628(85);
    return 1;
}

u32 native_ov007_021d82d8(void) {
    u32 result = 0;
    s32 value = func_ov007_021d86ac(data_ov007_021da0f4[2]);
    u16 *input = func_0202a634();
    if ((input[1] & 1) && value != -1) {
        func_0205be34(value);
        func_0205bdfc(value);
        func_020c20f4(data_ov007_021da0f4[2]);
        func_0205bf2c(5);
        func_0205c060(func_ov007_021d86c4(data_ov007_021da0f4[2]));
        func_020c211c(data_ov007_021da0f4[2]);
        value = func_ov007_021d876c(data_ov007_021da0f4[2]);
        if (value > 0) {
            func_0203d0d8(value, 1);
        }
        func_ov007_021d9628(82);
        result = 1;
    }
    return result;
}
