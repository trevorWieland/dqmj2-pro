typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;

extern s32 data_ov007_021db2c8[];
extern void func_ov007_021d93ac(u32, u32);
extern void func_ov007_021d93dc(u32, u32, u32);
extern void func_ov007_021d9400(u32, s32, s32);

void native_ov007_021d9ccc(u32 kind, u32 reverse, s32 duration, u8 x, u8 y) {
    s32 first;
    s32 second;
    s32 amount;
    float value;
    func_ov007_021d93ac(kind, 1);
    func_ov007_021d93dc(kind, x, y);
    first = 256 - y;
    second = y + 64;
    if ((float)(second < first ? second : first) / 80.0f > 0.0f) {
        value = 0.5f + 4096.0f * ((float)(second < first ? second : first) / 80.0f);
    } else {
        value = 4096.0f * ((float)(second < first ? second : first) / 80.0f) - 0.5f;
    }
    amount = (s32)value;
    data_ov007_021db2c8[3] = amount;
    if (reverse == 0) {
        func_ov007_021d9400(kind, 0, 0);
    } else {
        func_ov007_021d9400(kind, amount, amount);
    }
    data_ov007_021db2c8[1] = 0;
    data_ov007_021db2c8[2] = duration;
    ((u8 *)data_ov007_021db2c8)[0] = kind;
    data_ov007_021db2c8[4] = reverse;
    if (kind == 0) {
        volatile u16 *blend = (volatile u16 *)0x0400004A;
        volatile u32 *display = (volatile u32 *)0x04000000;
        *blend = (*blend & ~0x3F) | 0x3F;
        *blend = (*blend & ~0x3F00) | 0x1F00;
        *display = (*display & ~0xE000) | 0x8000;
    } else {
        volatile u16 *blend = (volatile u16 *)0x0400104A;
        volatile u32 *display = (volatile u32 *)0x04001000;
        *blend = (*blend & ~0x3F) | 0x3F;
        *blend = (*blend & ~0x3F00) | 0x1F00;
        *display = (*display & ~0xE000) | 0x8000;
    }
}
