typedef signed int s32;
typedef unsigned int u32;
typedef unsigned short u16;
typedef unsigned char u8;

extern s32 data_ov007_021db2c8[];
extern void func_02041510(u32, u32, u32);
extern void func_02041538(u32, u32, u32);
extern s32 func_02026144(s32, s32);
extern void func_ov007_021d9400(u32, s32, s32);
extern void func_ov007_021d93ac(u32, u32);
extern void func_02041898(u32);
extern void func_020418b0(u32);

void native_ov007_021d9e68(void) {
    s32 value;
    u32 kind;
    if (data_ov007_021db2c8[1] > data_ov007_021db2c8[2]) {
        return;
    }
    if (data_ov007_021db2c8[1] == 0 && data_ov007_021db2c8[4] == 1) {
        if (((u8 *)data_ov007_021db2c8)[0] == 0) {
            func_02041510(1, 2, 5);
        } else {
            func_02041538(1, 2, 5);
        }
    }
    if (data_ov007_021db2c8[4] == 0) {
        if (data_ov007_021db2c8[1] > 1) {
            value = func_02026144(data_ov007_021db2c8[3] * data_ov007_021db2c8[1], data_ov007_021db2c8[2]);
            func_ov007_021d9400(((u8 *)data_ov007_021db2c8)[0], value, value);
        } else {
            func_ov007_021d9400(((u8 *)data_ov007_021db2c8)[0], 0, 0);
        }
    } else {
        if (data_ov007_021db2c8[1] <= data_ov007_021db2c8[2] - 3) {
            value = func_02026144(data_ov007_021db2c8[3] * (data_ov007_021db2c8[2] - data_ov007_021db2c8[1]), data_ov007_021db2c8[2]);
            func_ov007_021d9400(((u8 *)data_ov007_021db2c8)[0], value, value);
        } else {
            func_ov007_021d9400(((u8 *)data_ov007_021db2c8)[0], 0, 0);
        }
    }
    data_ov007_021db2c8[1] = data_ov007_021db2c8[1] + 1;
    if (data_ov007_021db2c8[4] == 0 && data_ov007_021db2c8[1] == data_ov007_021db2c8[2] - 10) {
        if (((u8 *)data_ov007_021db2c8)[0] == 0) {
            func_02041510(0, 2, 10);
        } else {
            func_02041538(0, 2, 10);
        }
    }
    if (data_ov007_021db2c8[1] > data_ov007_021db2c8[2]) {
        func_ov007_021d93ac(((u8 *)data_ov007_021db2c8)[0], 0);
        kind = ((u8 *)data_ov007_021db2c8)[0];
        if (kind == 0) {
            volatile u32 *display = (volatile u32 *)0x04000000;
            volatile u16 *blend = (volatile u16 *)0x0400004A;
            *display = *display & ~0xE000;
            *blend = (*blend & ~0x3F00) | 0x3F00;
        } else {
            volatile u32 *display = (volatile u32 *)0x04001000;
            volatile u16 *blend = (volatile u16 *)0x0400104A;
            *display = *display & ~0xE000;
            *blend = (*blend & ~0x3F00) | 0x3F00;
        }
        if (data_ov007_021db2c8[4] == 1) {
            if (kind == 0) {
                func_02041898(2);
            } else {
                func_020418b0(2);
            }
        }
    }
}
