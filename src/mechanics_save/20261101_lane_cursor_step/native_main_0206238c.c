typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0202a634(void);
extern u32 native_fn_02062090(void);
extern u32 native_fn_02061270(void);
extern u32 native_fn_02061294(void);
extern u32 native_fn_02062520(void);
extern u32 native_fn_02062368(s8);
extern u32 native_fn_0205e7a8(u32, u32);
extern u8 native_data_021b9bd4[];
u32 native_main_0206238c(s8 *value, s32 lower, s32 upper) {
    u16 *input;
    s8 step;
    u16 buttons;
    input = (u16 *)native_fn_0202a634();
    step = 0;
    if (native_fn_02062090() == 0) return step;
    if (native_fn_02061270() != 0) return step;
    if (native_fn_02061294() != 0) return step;
    if (native_fn_02062520() == 0) return step;
    if ((s8)native_data_021b9bd4[0x2A1] != 42) return step;
    buttons = input[3];
    if (buttons & 0x200) step--;
    if ((buttons & 0x100) || (s8)native_data_021b9bd4[0x271] != 0) {
        step++;
        native_fn_02062368(0);
    }
    *value += step;
    if ((s32)*value < lower) *value = (s8)upper;
    if ((s32)*value > upper) *value = (s8)lower;
    if (step != 0) native_fn_0205e7a8(0xFFFFFFFFU, 0x56);
    return step;
}
