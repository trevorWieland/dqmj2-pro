typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef float f32;
typedef double f64;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
#define MULT_HI(a, b) ((s32)(((s64)(s32)(a) * (s32)(b)) >> 32))
#define MULTU_HI(a, b) ((u32)(((u64)(u32)(a) * (u32)(b)) >> 32))
#define ROTATE_RIGHT(value, amount) (((u32)(value) >> ((u32)(amount) & 31)) | ((u32)(value) << ((0U - (u32)(amount)) & 31)))
#define NULL ((void *)0)
typedef struct NativeVector {s32 x,y,z;} NativeVector;
typedef struct NativeMotion {u8 opaque00[0x10];s16 field10,field12;u8 opaque14[8];s16 field1c,field1e;u32 field20;u8 opaque24[4];u32 field28;u8 opaque2c[0x14];NativeVector field40,field4c;} NativeMotion;
extern u32 native_fn_0202a634();
extern u32 native_fn_020404e0();
extern u32 native_fn_020404f0();
extern u32 native_fn_02041510();
extern u32 native_fn_02041560();
extern u32 native_fn_020418e8();
extern u32 native_fn_02066c3c();
extern u32 native_fn_ov000_021df1f0(void);
extern u32 native_fn_ov000_021df3bc(s32);
extern u32 native_fn_ov000_021e7b9c();
extern u32 native_fn_ov000_02218800();
extern u32 native_fn_ov000_0221993c();
extern void native_fn_ov000_02219ce4(NativeVector*);
extern NativeMotion native_data_ov000_02245e54;
#define native_data_ov000_02245ea0 (native_data_ov000_02245e54.field4c)
