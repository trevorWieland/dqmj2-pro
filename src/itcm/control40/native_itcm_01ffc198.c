typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { s32 value; u32 ticks; } Status;
extern Status *native_fn_01ffbb38(void);
extern s32 native_fn_02067dd4(void);
extern s32 *native_fn_020894c8(void);
extern u32 native_fn_020271c8(void);
extern void native_fn_020271d8(void);
extern u32 native_fn_020ba598(u32, const void *, const s32 *);
extern u32 native_fn_020ba7c4(u32, u32, u32, u32, u32, u32);
extern void native_fn_01ffbfbc(void);
extern void native_fn_01ffbffc(void);
extern void native_fn_01ffc194(void);
extern void native_fn_01ffc184(void);
extern s32 native_data_01fffaac;
extern s32 native_data_01fffaa8;
extern u32 native_data_01fffab8[2];
extern u8 native_data_020e2c80[];
extern u8 native_data_020e2c8c[];
extern u8 native_data_020e2c98[];
extern u8 native_data_020e2ca4[];
u32 native_itcm_01ffc198(void) {
    Status *record;
    record = native_fn_01ffbb38();
    record->value = native_fn_02067dd4();
    native_fn_01ffbb38()->ticks = 0;
    native_data_01fffaac = *native_fn_020894c8();
    native_data_01fffaa8 = native_fn_01ffbb38()->value / 10;
    if (native_fn_020271c8() == 0) {
        native_data_01fffab8[0] = native_fn_020ba598(0, native_data_020e2c80, &native_data_01fffaac);
        native_data_01fffab8[1] = native_fn_020ba598(0, native_data_020e2c8c, &native_data_01fffaa8);
        native_fn_020271d8();
    } else {
        native_fn_020ba598((u8)native_data_01fffab8[0], native_data_020e2c98, &native_data_01fffaac);
        native_fn_020ba598((u8)native_data_01fffab8[1], native_data_020e2ca4, &native_data_01fffaa8);
    }
    return native_fn_020ba7c4(2, (u32)native_fn_01ffbfbc, (u32)native_fn_01ffbffc, (u32)native_fn_01ffc194, (u32)native_fn_01ffc184, 0x2710);
}
