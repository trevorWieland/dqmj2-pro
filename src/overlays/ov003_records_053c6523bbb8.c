typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;

extern void func_020c3528(void);
extern u8 *func_02062a50(u32);
extern u8 *func_02062a88(u32);
extern void func_020c357c(void *, u32);
extern void func_020c35b4(void *, u32);
extern u32 func_02062ad0(void);
extern u32 func_02062a78(u32);
extern u32 func_02062a68(u32);
extern void func_020c3790(void *);
extern void func_020c384c(u32);
extern u32 func_02062aa0(void);
extern void func_02008d78(void *, u32, u32);
extern void func_020c386c(void *);
extern void func_020c3928(u32);
extern void func_020c35ec(u32);
extern void func_020c360c(u32);
extern void func_020c362c(u32);
extern void func_020c364c(u32);
extern void func_020c366c(u32);
extern void func_020c368c(u32);
extern void func_020628b0(u32);
extern void func_02062980(u32);
extern u32 *func_020c35a0(u32);
extern u32 *func_020c35d8(u32);
extern void func_02062850(u32);
extern void func_02062904(u32);
extern void func_02008e0c(void *, void *, u32);
extern void func_0207b460(s16, u32, void *, void *);
extern u32 func_0207c2b8(void *, void *);
extern u32 func_0207c3d8(void *, void *);

void native_ov003_021d744c(void) {
    u8 index;
    u32 slots[3];
    u8 *record;
    func_020c3528();
    for (index = 0; index < 3; index++) {
        func_020c357c(func_02062a50(index), index);
    }
    for (index = 0; index < 3; index++) {
        func_020c35b4(func_02062a88(index), index);
    }
    for (index = 0; index < 3; index++) {
        record = func_02062a50(index);
        if (!record) {
            break;
        }
        record[49] = 0;
    }
    for (index = 0; index < 3; index++) {
        record = func_02062a88(index);
        if (!record) {
            break;
        }
        record[49] = 0;
    }
    if (func_02062ad0()) {
        for (index = 0; index < 3; index++) {
            slots[index] = func_02062a78(index);
        }
        func_020c3790(slots);
        func_020c384c((u8)func_02062ad0());
    } else {
        for (index = 0; index < 3; index++) {
            slots[index] = func_02062a68(index);
        }
        func_020c3790(slots);
        func_020c384c((u8)func_02062aa0());
    }
    func_02008d78(slots, 0, 12);
    func_020c386c(slots);
    func_020c3928(0);
    func_020c35ec(0);
    func_020c360c(2);
    func_020c362c(0);
    func_020c364c(2);
    func_020c366c(1);
    func_020c368c(2);
}

void native_ov003_021d75c8(void) {
    u8 index;
    u8 *destination;
    for (index = 0; index < 3; index++) {
        func_020628b0(0);
        func_02062980(0);
    }
    for (index = 0; index < 3; index++) {
        func_02062850(func_020c35a0(index)[5]);
        destination = func_02062a50(index);
        if (!destination) {
            break;
        }
        func_02008e0c(func_020c35a0(index), destination, 132);
    }
    for (index = 0; index < 3; index++) {
        func_02062904(func_020c35d8(index)[5]);
        destination = func_02062a88(index);
        if (!destination) {
            break;
        }
        func_02008e0c(func_020c35d8(index), destination, 132);
    }
}

void native_ov003_021d790c(void) {
    u8 index;
    u8 buffer[64];
    u8 *record;
    for (index = 0; index < 3; index++) {
        record = func_02062a50(index);
        if (record) {
            func_0207b460(*(s16 *)(record + 24), record[26], record + 122, buffer);
            *(u16 *)(record + 36) = func_0207c2b8(record + 32, buffer);
            *(u16 *)(record + 38) = func_0207c3d8(record + 32, buffer);
            record[51] = 0;
        }
    }
    for (index = 0; index < 3; index++) {
        record = func_02062a88(index);
        if (record) {
            func_0207b460(*(s16 *)(record + 24), record[26], record + 122, buffer);
            *(u16 *)(record + 36) = func_0207c2b8(record + 32, buffer);
            *(u16 *)(record + 38) = func_0207c3d8(record + 32, buffer);
            record[51] = 0;
        }
    }
}
