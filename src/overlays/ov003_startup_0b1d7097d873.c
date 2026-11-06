typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;

extern u8 data_ov003_021e0440[];
extern u8 data_ov003_021e0450[];
extern u8 data_ov003_021e0220[];
extern u8 data_ov003_021e0210[];
extern u8 data_ov003_021e020c[];
extern void func_0202a090(u32, u32);
extern u32 func_0202a1e0(u32);
extern void func_ov003_021d7694(void);
extern void func_ov003_021d7724(void);
extern void func_0207a9ec(u32);
extern void func_020c39d0(u32);
extern void func_ov003_021d790c(void);
extern u32 func_02027400(void);
extern void func_ov003_021d744c(void);
extern void func_ov003_021d7888(void);
extern void func_020c3a10(u32);
extern void func_0204617c(u32, u32);
extern void func_02084920(void);
extern void func_ov003_021d770c(void);
extern void func_ov003_021d8ce8(void);
extern void func_ov003_021d9dc0(void);
extern void func_02061898(void);
extern void func_020406a8(u32);
extern void func_0207aad0(u32);
extern void func_0202a164(u32);
extern void func_0205db90(void *, void *, u32);
extern u32 func_0205d9e8(u32, void *, void *, void *, u32);
extern void func_0205dbc4(u32, void *);
extern void func_0203cb2c(void);
extern void func_02002e5c(u32);
extern void func_020030ec(u32);
extern void func_02045338(void);
extern void func_020489f0(u32);
extern void func_0205fd80(u32);
extern void func_020bb334(void);
extern void func_02002c98(u32, u32, u32);
extern void func_02008c58(u32, u32, u32);
extern void func_02041898(u32);
extern void func_020414b0(u32);
extern void func_02046150(u32, u32, u32);
extern void func_020628b0(u32);
extern void func_02062980(u32);
extern u32 func_020c3704(u32);
extern void func_02062850(u32);
extern u32 func_020c3770(u32);
extern void func_02062904(u32);

void native_ov003_021d7240(void) {
    func_0202a090(1, 0x50000);
    func_0202a090(2, 0x29800);
    data_ov003_021e0440[0] = func_0202a1e0(1);
    func_ov003_021d7694();
    func_ov003_021d7724();
    func_0207a9ec(2);
    func_020c39d0(0);
    func_ov003_021d790c();
    if (func_02027400() == 1) {
        func_ov003_021d744c();
    } else if (func_02027400() == 2) {
        func_ov003_021d7888();
    }
    data_ov003_021e0440[2] = 0;
    data_ov003_021e0440[3] = 3;
    data_ov003_021e0440[4] = 3;
    data_ov003_021e0440[1] = 0;
}

void native_ov003_021d73e4(void) {
    func_020c39d0(0);
    func_020c3a10(1);
    func_0204617c(0, 2);
    func_02084920();
    func_ov003_021d770c();
    func_ov003_021d8ce8();
    func_ov003_021d9dc0();
    func_02061898();
    func_020406a8(1);
    func_0207aad0(2);
    func_0202a1e0(((s8 *)data_ov003_021e0440)[0]);
    func_0202a164(2);
    func_0202a164(1);
}

void native_ov003_021d770c(void) {
    void (*target)(u32, void *) = func_0205dbc4;
    target(2, data_ov003_021e0450);
}

void native_ov003_021d7724(void) {
    volatile u32 *display = (volatile u32 *)0x04000000;
    volatile u16 *bg = (volatile u16 *)0x04000008;
    func_0203cb2c();
    func_02002e5c(9);
    func_020030ec(2);
    func_02045338();
    func_020489f0(0);
    func_0205fd80(0);
    func_020bb334();
    func_02002c98(1, 3, 0);
    *display = (*display & 0xFFCFFFEF) | 0x10;
    bg[0] = (bg[0] & 0x43) | 0x318;
    bg[1] = (bg[1] & 0x43) | 0x108;
    bg[2] = (bg[2] & 0x43) | 0x210;
    bg[3] = (bg[3] & 0x43) | 0x4884;
    func_02008c58(0, 0x06000000, 0x80000);
    *display = (*display & ~0x1F00) | 0x1F00;
    func_02041898(2);
    func_020414b0(63);
    *(volatile u16 *)0x0400000A = *(volatile u16 *)0x0400000A & ~3;
    *(volatile u16 *)0x0400000E = (*(volatile u16 *)0x0400000E & ~3) | 3;
    *(volatile u16 *)0x0400000C = (*(volatile u16 *)0x0400000C & ~3) | 1;
    *(volatile u16 *)0x04000008 = (*(volatile u16 *)0x04000008 & ~3) | 2;
    *(volatile u32 *)0x0400001C = 0;
    *display = *display & ~0xE000;
    func_02046150(0, 0, 2);
}

u32 native_ov003_021d7868(void) {
    return ((s8 *)data_ov003_021e0440)[4];
}

void native_ov003_021d7878(u32 value) {
    data_ov003_021e0440[4] = value;
}

void native_ov003_021d7888(void) {
    u8 index;
    for (index = 0; index < 3; index++) {
        func_020628b0(0);
        func_02062980(0);
    }
    for (index = 0; index < 3; index++) {
        u32 pointer = func_020c3704(index);
        if (pointer) {
            func_02062850(pointer);
        }
    }
    for (index = 0; index < 3; index++) {
        u32 pointer = func_020c3770(index);
        if (pointer) {
            func_02062904(pointer);
        }
    }
}
