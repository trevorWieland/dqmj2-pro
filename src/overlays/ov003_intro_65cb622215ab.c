typedef unsigned int u32;
typedef signed char s8;
typedef struct { volatile s8 counter; unsigned char reserved[3]; u32 handle; u32 ready; u32 phase; } Intro;

extern u32 data_ov003_021e0440[];
extern Intro data_ov003_021e0454;
extern void func_ov003_021d7a48(void);
extern void func_0205e644(void);
extern void func_0205e66c(void);
extern void func_0205e73c(u32);
extern void func_0205e7a8(u32, u32);
extern void func_ov003_021d7a14(void);
extern u32 func_0205f5dc(void);
extern void func_0205f5f4(u32);
extern void func_020273d8(u32);
extern u32 func_02027400(void);
extern void func_ov003_021d7c98(void);
extern void func_02061238(u32, u32, u32);
extern void func_020406a8(u32);
extern void func_020612ec(u32, u32, u32, u32);
extern u32 func_ov003_021d7dac(void);
extern void func_02041510(u32, u32, u32);
extern u32 func_02041800(void);
extern void func_ov003_021d7dc8(void);
extern void func_0206157c(void);
extern u32 func_ov003_021d7868(void);
extern void func_ov003_021d7e04(void);
extern u32 func_ov003_021d7ee8(void);
extern void func_020c39d0(u32);
extern void func_ov003_021d7f90(void);
extern void func_020bb38c(u32, u32);
extern void func_020bb3f4(void);
extern void func_02008c58(u32, u32, u32);

void native_ov003_021d79e4(u32 sound) {
    func_ov003_021d7a48();
    func_0205e644();
    func_0205e66c();
    func_0205e73c(sound);
    func_0205e7a8(0, sound);
    func_ov003_021d7a14();
}

void native_ov003_021d7a14(void) {
    data_ov003_021e0440[3] = func_0205f5dc();
    func_0205e73c(181);
    func_0205e73c(147);
    data_ov003_021e0440[2] = 1;
}

void native_ov003_021d7a48(void) {
    if (data_ov003_021e0440[2] == 1) {
        func_0205f5f4(data_ov003_021e0440[3]);
    }
    data_ov003_021e0440[2] = 0;
}

void native_ov003_021d7a78(void) {
    func_020273d8(9);
    data_ov003_021e0454.handle = 0;
    if (func_02027400() == 2) {
        data_ov003_021e0454.ready = 0;
        func_ov003_021d7c98();
        data_ov003_021e0454.phase = 0;
    } else {
        func_02061238(1, 2, 0);
        func_020406a8(1);
        func_020612ec(34, 1, 32768, 0);
        data_ov003_021e0454.phase = 2;
    }
}

u32 native_ov003_021d7afc(void) {
    u32 result = 0;
    switch (data_ov003_021e0454.phase) {
        case 0:
            if (func_ov003_021d7dac()) {
                func_02041510(1, 2, 10);
                data_ov003_021e0454.phase = 1;
            }
            break;
        case 1:
            if (func_02041800() != 1) {
                func_ov003_021d7dc8();
                func_02061238(1, 2, 0);
                func_020406a8(1);
                func_020612ec(34, 1, 32768, 0);
                data_ov003_021e0454.phase = 2;
            }
            break;
        case 2:
            func_0206157c();
            if (func_ov003_021d7868() == 2) {
                data_ov003_021e0454.phase = 3;
            }
            break;
        case 3:
            if (func_02041800() != 1) {
                func_ov003_021d7e04();
                data_ov003_021e0454.phase = 4;
            }
            break;
        case 4:
            if (func_ov003_021d7ee8()) {
                data_ov003_021e0454.phase = 5;
            }
            break;
        case 5:
            data_ov003_021e0454.counter = data_ov003_021e0454.counter - 1;
            if (data_ov003_021e0454.counter == 0) {
                func_02041510(1, 2, 10);
                func_020c39d0(3);
            }
            if (data_ov003_021e0454.counter <= 0 && func_02041800() != 1) {
                func_ov003_021d7f90();
                result = 1;
            }
            break;
    }
    if (func_ov003_021d7868() == 1) {
        result = 1;
    }
    return result;
}

void native_ov003_021d7c70(void) {
    if (data_ov003_021e0454.handle) {
        func_020bb38c(data_ov003_021e0454.handle, 1);
        func_020bb3f4();
    }
}

u32 native_ov003_021d7dac(void) {
    return data_ov003_021e0454.ready != 0;
}

void native_ov003_021d7dc8(void) {
    func_020bb38c(data_ov003_021e0454.handle, 1);
    func_02008c58(0, 0x06000000, 0x80000);
    *(volatile u32 *)0x04000000 = *(volatile u32 *)0x04000000 & ~0xE000;
}

void native_ov003_021d7f90(void) {
    *(volatile u32 *)0x04000000 = *(volatile u32 *)0x04000000 & ~0xE000;
}

void native_ov003_021d7fa4(void) {
    data_ov003_021e0454.ready = 1;
}
