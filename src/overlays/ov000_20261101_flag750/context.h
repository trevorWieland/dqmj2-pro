typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef float f32;

typedef struct NativeVector {
    s32 x;
    s32 y;
    s32 z;
} NativeVector;

typedef struct NativeMotion {
    u8 opaque00[0x10];
    s16 field10;
    s16 field12;
    u8 opaque14[0xC];
    u32 field20;
    u8 opaque24[4];
    u32 field28;
    u8 opaque2c[0x14];
    NativeVector field40;
    NativeVector field4c;
} NativeMotion;

typedef struct NativeRow {
    u8 opaque00[4];
    s16 field04;
    s16 field06;
    u8 field08;
    u8 field09;
    s8 field0a;
    u8 opaque0b[3];
} NativeRow;

typedef char NativeVectorSize[(sizeof(NativeVector)==12)?1:-1];
typedef char NativeMotionSize[(sizeof(NativeMotion)==0x58)?1:-1];
typedef char NativeRowSize[(sizeof(NativeRow)==14)?1:-1];

extern f32 native_fn_02024e0c(f32,f32);
extern f32 native_fn_02025578(f32,f32);
extern s32 native_fn_020259b4(f32);
extern f32 native_fn_02025a28(s32);
extern f32 native_fn_02025ab8(f32,f32);
extern f32 native_fn_02025ca4(f32,f32);
extern u32 native_fn_02041f74(u32,NativeVector*);
extern u32 native_fn_ov000_021df1f0(void);
extern u32 native_fn_ov000_021df3bc(s32);
extern u8 *native_fn_ov000_021e07ac(void);
extern void native_fn_ov000_02219ce4(NativeVector*);
extern NativeMotion native_data_ov000_02245e54;
#define native_data_ov000_02245ea0 (native_data_ov000_02245e54.field4c)

typedef struct NativeFlagObject {
    u8 opaque00[0x7C];
    u32 field7c;
} NativeFlagObject;
typedef struct NativeResourceState {
    u32 field00;
    u8 opaque04[0x18];
    u32 field1c;
} NativeResourceState;
extern NativeResourceState native_data_ov000_02245f2c;
extern u32 native_fn_0205f98c(s32,s32);
extern u32 native_fn_ov000_022198ec(void);
