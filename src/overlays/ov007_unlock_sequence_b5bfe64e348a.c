typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { u32 sound; s32 timer; s32 blend; s32 index; u32 phase; u32 effect; } Sequence;

extern Sequence data_ov007_021db2b0;
extern s8 data_ov007_021da924;
extern s8 data_ov007_021da07c[10][5];
extern void func_ov007_021d9770(void);
extern u32 func_02041814(void);
extern void func_020042c4(void *, u32, u32, u32, u32);
extern u32 func_0205e814(u32, u32, u32);
extern u32 func_0205f35c(s32, u32);
extern void func_0205e7f4(u32, u32);
extern void func_0205f404(u32, u32);
extern void func_02041538(u32, u32, u32);
extern void func_0204157c(u32);
extern void func_020414c8(u32);
extern void func_ov007_021d929c(void);
extern u32 func_ov007_021d873c(s32);
extern u32 func_ov007_021d8634(s32);
extern u32 func_ov007_021d864c(s32);
extern void func_ov007_021d95b0(u32, u32);
extern void func_ov007_021d9628(u32);
extern void func_ov007_021d932c(s32, u32);
extern void func_ov007_021d8724(s32, u32);
extern void func_02041908(u32, u32);
extern void func_020418b0(u32);
extern void func_ov007_021d91f4(void);
extern void func_ov007_021d9854(void);
extern void func_ov007_021d95ec(void);

u32 native_ov007_021d9858(void) {
    s32 value;
    u32 first;
    u32 second;
    if (data_ov007_021db2b0.phase == 0) {
        func_ov007_021d9770();
        data_ov007_021db2b0.blend = 16;
        data_ov007_021db2b0.index = 0;
        data_ov007_021db2b0.phase = 5;
    } else if (data_ov007_021db2b0.phase == 5) {
        if (func_02041814() != 1) {
            func_020042c4((void *)0x04001050, 4, 2, data_ov007_021db2b0.blend, 0);
            data_ov007_021db2b0.phase = 7;
            data_ov007_021db2b0.timer = 30;
            data_ov007_021db2b0.sound = func_0205e814(0, 0, 30);
        }
    } else if (data_ov007_021db2b0.phase == 7) {
        if (data_ov007_021db2b0.timer-- <= 0) {
            data_ov007_021db2b0.phase = 10;
            data_ov007_021db2b0.timer = 60;
            data_ov007_021db2b0.effect = func_0205f35c(-1, 170);
            func_0205e7f4(0, 1);
        }
    } else if (data_ov007_021db2b0.phase == 10) {
        *(volatile u16 *)0x04001052 = data_ov007_021db2b0.blend | ((16 - data_ov007_021db2b0.blend) << 8);
        data_ov007_021db2b0.timer = data_ov007_021db2b0.timer - 1;
        data_ov007_021db2b0.blend = data_ov007_021db2b0.timer * 16 / 60;
        if (data_ov007_021db2b0.timer < 0) {
            data_ov007_021db2b0.phase = 15;
            *(volatile u32 *)0x04001000 = (*(volatile u32 *)0x04001000 & ~0x1F00) | 0x1200;
            func_0205f404(data_ov007_021db2b0.effect, 10);
            func_02041538(1, 2, 15);
            func_0204157c(6);
        }
    } else if (data_ov007_021db2b0.phase == 15) {
        if (func_02041814() != 1) {
            data_ov007_021db2b0.phase = 18;
            func_020414c8(6);
            func_02041538(1, 2, 1);
            func_0204157c(6);
            func_ov007_021d929c();
        }
    } else if (data_ov007_021db2b0.phase == 18) {
        value = data_ov007_021da07c[data_ov007_021da924][data_ov007_021db2b0.index];
        if (func_ov007_021d873c(value)) {
            data_ov007_021db2b0.phase = 25;
            data_ov007_021db2b0.timer = 0;
        } else {
            first = func_ov007_021d8634(value);
            second = func_ov007_021d864c(value);
            func_ov007_021d95b0(first, second);
            data_ov007_021db2b0.phase = 20;
            data_ov007_021db2b0.timer = 32;
        }
    } else if (data_ov007_021db2b0.phase == 20) {
        if (data_ov007_021db2b0.timer-- <= 0) {
            func_ov007_021d9628(92);
            func_ov007_021d932c(data_ov007_021da07c[data_ov007_021da924][data_ov007_021db2b0.index], 1);
            func_ov007_021d8724(data_ov007_021da07c[data_ov007_021da924][data_ov007_021db2b0.index], 1);
            data_ov007_021db2b0.phase = 25;
            data_ov007_021db2b0.timer = 10;
        }
    } else if (data_ov007_021db2b0.phase == 25) {
        if (data_ov007_021db2b0.timer-- <= 0) {
            data_ov007_021db2b0.index++;
            if (data_ov007_021da07c[data_ov007_021da924][data_ov007_021db2b0.index] != -1) {
                data_ov007_021db2b0.phase = 18;
            } else {
                data_ov007_021db2b0.phase = 30;
                data_ov007_021db2b0.timer = 0;
                func_02041538(0, 2, 60);
                func_02041908(60, 6);
                func_0205e7f4(0, 0);
                func_0205e814(0, data_ov007_021db2b0.sound, 60);
            }
        }
    } else if (data_ov007_021db2b0.phase == 30) {
        if (func_02041814() != 1) {
            func_020414c8(63);
            func_020418b0(0);
            func_ov007_021d91f4();
            data_ov007_021db2b0.phase = 40;
        }
    } else if (data_ov007_021db2b0.phase == 40) {
        data_ov007_021db2b0.phase = 0;
        func_ov007_021d9854();
        return 1;
    }
    func_ov007_021d95ec();
    return 0;
}
