typedef unsigned int u32;
typedef unsigned short u16;
typedef signed int s32;
typedef struct {
    u32 channel : 5;
    u32 flag : 1;
    u32 payload : 26;
} FifoWord;
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);
s32 native_main_0200a440(u32 channel, u32 payload, u32 flag) {
    FifoWord word;
    u32 irq;
    word.channel = channel;
    word.flag = flag;
    word.payload = payload;
    if (*(volatile u16 *)0x04000184 & 0x4000) {
        *(volatile u16 *)0x04000184 |= 0xC000;
        return -1;
    }
    irq = native_fn_02007ff4();
    if (*(volatile u16 *)0x04000184 & 2) {
        native_fn_02008008(irq);
        return -2;
    } else {
        *(volatile FifoWord *)0x04000188 = word;
        native_fn_02008008(irq);
        return 0;
    }
}
