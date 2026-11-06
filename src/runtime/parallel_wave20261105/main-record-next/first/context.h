typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef struct NativeBits {
    s8 bit0:1;
    s8 bit1:1;
    s8 bit2:1;
    s8 bit3:1;
    s8 bit4:1;
    s8 bit5:1;
    s8 bit6:1;
    s8 bit7:1;
} NativeBits;
typedef struct NativeState {
    u8 reserved0000[0xd1];
    NativeBits field00d1;
} NativeState;
typedef struct NativeSmallState {
    u8 field0000;
    s8 field0001;
    u8 field0002;
    u8 field0003;
} NativeSmallState;
extern NativeSmallState native_data_021d6620;
extern NativeState native_data_021d6630;
extern u8 native_data_021d6714;
extern u8 native_data_021d65f0[],native_data_021d65fc[];
extern u8 native_data_021d6608[],native_data_021d6614[];
extern u32 native_fn_02048f6c(int);
extern int native_fn_02065730(void*,int,int,int,int);
extern u32 native_fn_020cd4e8(u32,u32);
extern u32 native_fn_020c48f8(s8);
extern u32 native_fn_020cb42c(int);
extern int native_fn_020cb5c4(int,s8*,s8*,s8*);
extern u32 native_fn_020cb2fc(void);
