typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef struct NativeSettingTarget {
    u8 opaque[0x32a];
    s16 value;
} NativeSettingTarget;
extern NativeSettingTarget *native_host_arm7_data_0380fff4;
extern volatile u16 native_host_arm7_data_0480802c;
