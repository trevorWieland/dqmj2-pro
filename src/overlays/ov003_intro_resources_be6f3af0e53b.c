typedef unsigned int u32;
typedef unsigned short u16;
typedef signed char s8;
typedef struct { volatile s8 counter; unsigned char reserved[3]; u32 handle; u32 ready; u32 phase; } Intro;

extern Intro data_ov003_021e0454;
extern char data_ov003_021e022c[];
extern char data_ov003_021e0238[];
extern char data_ov003_021e0248[];
extern char data_ov003_021e0258[];
extern char data_ov003_021e0268[];
extern u32 func_020653d0(void);
extern void func_0201d444(void *, const void *, ...);
extern u32 func_020bb338(void *, u32);
extern void func_020bb3cc(u32);
extern void func_020bb38c(u32, u32);
extern void func_020414b0(u32);
extern void func_02041510(u32, u32, u32);
extern void func_020456ac(u32, u32, u32, u32, u32, u32);
extern void func_0205e7a8(u32, u32);
extern void func_0205e814(u32, u32, u32);

void native_ov003_021d7c98(void) {
    char buffer[32];
    u32 mode = func_020653d0();
    switch(mode) {
    case 0:
        func_0201d444(buffer, data_ov003_021e022c);
        break;
    case 5:
        func_0201d444(buffer, data_ov003_021e0238);
        break;
    default:
        func_0201d444(buffer, data_ov003_021e0248);
        break;
    }
    data_ov003_021e0454.handle = func_020bb338(buffer, 1);
    if (data_ov003_021e0454.handle) {
        func_020bb3cc(data_ov003_021e0454.handle);
    }
    func_020414b0(63);
    func_02041510(0, 2, 10);
    *(volatile u32 *)0x04000000 = (*(volatile u32 *)0x04000000 & ~0x1F00) | 0xA00;
    *(volatile u16 *)0x04000048 = (*(volatile u16 *)0x04000048 & ~0x3F) | 0x28;
    *(volatile u16 *)0x0400004A = (*(volatile u16 *)0x0400004A & ~0x3F) | 0x2A;
    *(volatile u16 *)0x04000040 = 255;
    *(volatile u16 *)0x04000044 = 5311;
    *(volatile u32 *)0x04000000 = (*(volatile u32 *)0x04000000 & ~0xE000) | 0x2000;
    func_020456ac(0, 1, 0, 4, 32, 24);
}

u32 native_ov003_021d7e04(void) {
    char buffer[32];
    func_0201d444(buffer, data_ov003_021e0258);
    data_ov003_021e0454.handle = func_020bb338(buffer, 1);
    if (data_ov003_021e0454.handle) {
        func_020bb3cc(data_ov003_021e0454.handle);
    }
    func_020414b0(63);
    func_02041510(0, 2, 10);
    *(volatile u32 *)0x04000000 = (*(volatile u32 *)0x04000000 & ~0x1F00) | 0xA00;
    *(volatile u16 *)0x04000048 = (*(volatile u16 *)0x04000048 & ~0x3F) | 0x28;
    *(volatile u16 *)0x0400004A = (*(volatile u16 *)0x0400004A & ~0x3F) | 0x2A;
    *(volatile u16 *)0x04000040 = 255;
    *(volatile u16 *)0x04000044 = 5311;
    *(volatile u32 *)0x04000000 = (*(volatile u32 *)0x04000000 & ~0xE000) | 0x2000;
    func_020456ac(0, 1, 0, 4, 32, 24);
    data_ov003_021e0454.counter = 40;
    return 1;
}

u32 native_ov003_021d7ee8(void) {
    char buffer[32];
    data_ov003_021e0454.counter = data_ov003_021e0454.counter - 1;
    if (data_ov003_021e0454.counter == 0) {
        func_0201d444(buffer, data_ov003_021e0268);
        func_020bb38c(data_ov003_021e0454.handle, 1);
        data_ov003_021e0454.handle = func_020bb338(buffer, 1);
        if (data_ov003_021e0454.handle) {
            func_020bb3cc(data_ov003_021e0454.handle);
        }
        func_0205e7a8(-1, 147);
        func_0205e814(0, 0, 30);
        data_ov003_021e0454.counter = 40;
        return 1;
    }
    return 0;
}
