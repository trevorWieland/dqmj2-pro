typedef unsigned char u8;
typedef unsigned int u32;
typedef int s32;
extern u32 *native_fn_020633b0(void);
extern void native_fn_02008d78(void *, u32, u32);
extern u32 native_fn_first_02062a10(u32);
extern u32 native_fn_second_02062a10(u32);
extern void native_fn_02046af4(u32, u32, u32, u32, u8 *, u32);
extern void native_fn_020bb1b4(u32, u8 **, u8 *, u8 *);
extern u8 native_data_01fffab0[];
extern u8 native_data_01fffae0[];
extern u8 *native_data_01fffac8[];
extern u8 native_data_01fffaa4[];

void native_itcm_01ffc654(void) {
    u32 *context;
    s32 index;
    u8 *output;
    u32 value;
    context = native_fn_020633b0();
    native_fn_02008d78(native_data_01fffab0, 0, 6);
    native_fn_02008d78(native_data_01fffae0, 0, 192);
    output = native_data_01fffae0;
    for (index = 0; index < 6; index++, output += 32) {
        native_data_01fffac8[index] = output;
        if (index < 3) {
            value = native_fn_first_02062a10(context[7 + index]);
        } else {
            value = native_fn_second_02062a10(context[7 + index]);
        }
        if (value) {
            native_fn_02046af4(0, value, 0, 0, output, 255);
        }
    }
    native_fn_020bb1b4(6, native_data_01fffac8, native_data_01fffab0, native_data_01fffaa4);
}
