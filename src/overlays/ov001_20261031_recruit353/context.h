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
extern u32 native_fn_020443ec();
extern u32 native_fn_02044424();
extern u32 native_fn_02061238();
extern u32 native_fn_0206271c();
extern u32 native_fn_02062a10();
extern u32 native_fn_02062d24();
extern u32 native_fn_02062e44();
extern u32 native_fn_02062fd4();
extern u32 native_fn_02063038();
extern u32 native_fn_02063050();
extern u32 native_fn_02063068();
extern u32 native_fn_02063080();
extern u32 native_fn_0207a9ec();
extern u32 native_fn_0207b460();
extern u32 native_fn_0207c2b8();
extern u32 native_fn_0207c3d8();
extern u8 *native_fn_ov001_021fbe70(void);
extern u8 native_data_ov001_0223def8[];
