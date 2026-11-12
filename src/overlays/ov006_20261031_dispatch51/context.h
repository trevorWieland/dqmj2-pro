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
extern u32 native_fn_020048a0();
extern u32 native_fn_020048f4();
extern u32 native_fn_0200494c();
extern u32 native_fn_020049a4();
extern u32 native_fn_02004aa8();
extern u32 native_fn_02004b00();
extern u32 native_fn_02004c78();
extern u32 native_fn_02004f78();
extern u32 native_fn_02004fd8();
extern u32 native_fn_ov006_021f26e4();
extern u32 native_fn_ov006_021f2798();
extern u32 native_fn_ov006_021f27d4();
extern u32 native_fn_ov006_021f2920();
extern u32 native_fn_ov006_021f2a74();
extern u32 ov006_main_loop_set_callback_021f52cc();
extern u32 native_fn_ov006_021f5328();
extern u32 native_fn_ov006_021f5334();
extern u32 native_fn_ov006_021f5344();
extern u32 native_fn_ov006_021f5394();
extern u32 native_fn_ov006_021f53c8();
extern u32 native_fn_ov006_021f59d8();
extern u32 native_fn_ov006_021fed84();
extern u32 native_fn_ov006_02202fb8();
extern u32 native_fn_ov006_02203908();
extern u8 native_data_ov006_0220da64[];
extern u8 native_data_ov006_0220da80[];
extern u8 native_data_ov006_0220da90[];
extern u8 native_data_ov006_0220daa4[];
extern u8 native_data_ov006_0220dab8[];
extern u8 native_data_ov006_0220dacc[];
extern u8 native_data_ov006_0220dae0[];
extern u8 native_data_ov006_0220daf8[];
extern u8 native_data_ov006_0220db10[];
extern u8 native_data_ov006_0220db28[];
extern u8 native_data_ov006_0220db40[];
extern u8 native_data_ov006_0220db58[];
extern u8 native_data_ov006_0220db70[];
extern u8 native_data_ov006_0220db84[];
extern u8 native_data_ov006_0221c098[];
