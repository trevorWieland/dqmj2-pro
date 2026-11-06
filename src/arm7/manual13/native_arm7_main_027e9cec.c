typedef unsigned int u32;
typedef unsigned short u16;
extern u16 native_arm7_data_04808040[];
u32 native_arm7_main_027e9cec(u16 value) {
    *native_arm7_data_04808040 = value;
    return 0;
}
