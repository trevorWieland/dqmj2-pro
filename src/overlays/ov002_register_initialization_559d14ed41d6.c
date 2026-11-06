typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;

typedef struct { u32 control; u32 pad4; u16 bg[4]; u8 pad16[12]; u32 word28; } Registers;

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
extern void func_02002d00(u32);
extern void func_020038a8(u32);
extern void func_02003950(u32);
extern void func_020039c0(u32);
extern void func_02003a40(u32);
extern void func_02045680(u32);
extern u32 *func_02049ad0(s8);
extern void func_02048e8c(void);

void native_ov002_021d9ca4(void) {
    s8 index;
    func_02002d00(0);
    ((volatile Registers *)0x04001000)->control = (((volatile Registers *)0x04001000)->control & 0xffcfffef) | 0x10;
    func_020038a8(4);
    func_02003950(256);
    func_020039c0(0);
    func_02003a40(0);
    ((volatile Registers *)0x04001000)->bg[0] = (((volatile Registers *)0x04001000)->bg[0] & 0x43) | 0x11c;
    ((volatile Registers *)0x04001000)->bg[1] = (((volatile Registers *)0x04001000)->bg[1] & 0x43) | 0x14;
    ((volatile Registers *)0x04001000)->bg[2] = (((volatile Registers *)0x04001000)->bg[2] & 0x43) | 0x208;
    ((volatile Registers *)0x04001000)->bg[3] = (((volatile Registers *)0x04001000)->bg[3] & 0x43) | 0x304;
    func_02008c58(0, 0x06200000, 0x20000);
    func_02008c58(0, 0x06600000, 0x20000);
    func_02008c58(0, 0x05000400, 0x400);
    func_02008c58(0, 0x07000400, 0x400);
    func_02045680(0);
    func_02045680(1);
    func_02045680(2);
    func_02045680(3);
    ((volatile u16 *)0x04001008)[0] &= ~3;
    ((volatile u16 *)0x04001008)[2] = (((volatile u16 *)0x04001008)[2] & ~3) | 1;
    ((volatile u16 *)0x04001008)[3] = (((volatile u16 *)0x04001008)[3] & ~3) | 2;
    ((volatile u16 *)0x04001008)[1] = (((volatile u16 *)0x04001008)[1] & ~3) | 3;
    *(volatile u32 *)((u8 *)0x04001008 - 8) = (*(volatile u32 *)((u8 *)0x04001008 - 8) & ~0x1f00) | 0x1f00;
    func_02045338();
    func_020489f0(1);
    func_0205fd80(1);
    index = 0;
    do {
        u32 *object = func_02049ad0(index);
        ((u8 *)object)[4] = 31;
        ((u8 *)object)[5] = 127;
        object[0] = 0;
        ((s8 *)object)[6] = -1;
        index++;
    } while (index < 36);
    func_02046150(1, 0, 2);
    func_02046150(2, 2, 2);
    func_02048e8c();
}
