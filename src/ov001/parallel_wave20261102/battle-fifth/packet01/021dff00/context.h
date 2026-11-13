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
extern u32 native_fn_0202ac08(void *arg0);
extern u32 native_fn_0202ac4c(void *arg0);
extern u32 native_fn_0205d6f4(s32 arg0);
extern u32 native_fn_0205d718(u32 arg0);
extern u32 native_fn_0205d790(u32 arg0);
extern u32 native_fn_ov001_021d7e80(void *arg0);
extern u32 native_fn_ov001_021db788(u32 arg0,u32 arg1);
extern u32 native_fn_ov001_021dbb9c(u32 arg0,u32 arg1);
extern u32 native_fn_ov001_021dc230(u32 arg0,u32 arg1);
extern u32 native_fn_ov001_021eea10(u32 arg0,u32 arg1);
extern u32 native_fn_ov001_021eeb70(u32 arg0);
extern s32 ov001_effect_resource_create_021eec7c(u32 arg0,u8 *arg1,s32 arg2);
typedef struct {
    u8 unknown_0[0x8];
    s8 field_8;
    u8 unknown_9[0x21];
    u8 field_2a;
    s8 field_2b;
    s8 field_2c;
    u8 unknown_2d[0x53];
    s32 field_80;
} Record_native_data_ov001_022388ec;
extern Record_native_data_ov001_022388ec native_data_ov001_022388ec;
extern u32 native_data_ov001_0223896c[];
extern u8 native_data_ov001_02238988[];
typedef char Field_2a_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec *)0)->field_2a==0x2a)?1:-1];
typedef char Field_2b_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec *)0)->field_2b==0x2b)?1:-1];
typedef char Field_2c_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec *)0)->field_2c==0x2c)?1:-1];
typedef char Field_80_LayoutCheck[((u32)&((Record_native_data_ov001_022388ec *)0)->field_80==0x80)?1:-1];
typedef char ActorPointerWordSizeCheck[(sizeof(native_data_ov001_0223896c[0])==4)?1:-1];
