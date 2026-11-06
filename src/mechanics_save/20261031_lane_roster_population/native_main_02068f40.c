typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct { s8 first; u8 second; u8 third; u8 fourth; } NativeState;
extern NativeState native_data_021c4968;

u32 native_main_02068f40(u32 value) {
    native_data_021c4968.first = -1;
    native_data_021c4968.third = value;
    native_data_021c4968.fourth = 0;
    return 0;
}
