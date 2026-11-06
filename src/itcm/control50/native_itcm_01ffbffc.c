typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef int s32;
typedef struct {
    s32 value;
    u32 ticks;
} Status;
extern Status *native_fn_01ffbb38(void);
extern u8 *native_fn_02063f48(void);
extern s32 *native_fn_020894c8(void);
extern u32 native_fn_020ba5a4(s32, u8 *, u32);
extern u8 native_data_020e2c68[];
extern u8 native_data_020e2c74[];
extern s32 native_data_01ffbb04[];

u32 native_itcm_01ffbffc(s32 arg) {
    u32 count;
    s32 iteration;
    s32 current;
    s32 lower;
    s32 upper;
    u32 tag;
    u16 bits;
    u8 *record;
    current = native_fn_01ffbb38()->value / 10;
    record = native_fn_02063f48();
    tag = native_fn_020ba5a4(arg, native_data_020e2c68, 65535);
    native_fn_020ba5a4(arg, native_data_020e2c74, 65535);
    if (tag != (u32)*native_fn_020894c8()) {
        return 0;
    }
    if (native_fn_01ffbb38()->ticks > 3600) {
        return 0x7fffff;
    }
    bits = *(u16 *)(record + 0x1946);
    count = 0;
    iteration = 0;
    do {
        if (bits & 1) {
            count++;
        }
        bits >>= 1;
        iteration++;
    } while (iteration < 10);
    switch (count) {
    case 0:
    case 1:
        lower = 5;
        upper = 10;
        break;
    case 2:
    case 3:
        lower = 4;
        upper = 9;
        break;
    case 4:
    case 5:
        lower = 3;
        upper = 8;
        break;
    case 6:
    case 7:
        lower = 2;
        upper = 7;
        break;
    default:
        lower = 1;
        upper = 6;
        break;
    }
    if (native_fn_01ffbb38()->ticks > 1800) {
        lower--;
        upper++;
    }
    lower = (s32)((u32)current * (u32)native_data_01ffbb04[lower]) / 100;
    upper = (s32)((u32)current * (u32)native_data_01ffbb04[upper]) / 100;
    if (upper < current && lower > current) {
        return 0x7fffff;
    }
    return 0;
}
