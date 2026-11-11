/*
 * ov001 packet p4d: shared types and measured globals for the small ov001
 * accessor family at the start of unit ov001-u2.
 */
typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    u32 w0;
    u32 w1;
    u32 w2;
} Params;

typedef struct {
    s8 a;
    s8 b;
    s8 pad[2];
} PairEntry;

extern u8 native_data_ov001_0222ec84[];
extern u8 native_data_ov001_0222ec88[];
extern u8 native_data_ov001_0222ecb0[];
extern u8 native_data_ov001_02238ad4[];
extern u8 native_data_ov001_02238b44[];
extern u8 native_data_ov001_02238d1c[];
extern u8 native_data_ov001_02238d2e[];
extern u8 native_data_ov001_02238d40[];
extern u8 native_data_ov001_02238d58[];
extern u8 native_data_ov001_02238d7c[];
extern u8 native_data_ov001_02238dec[];
extern u8 native_data_ov001_02238f6c[];
extern u8 native_data_ov001_0223989c[];

extern u32 native_fn_020443ec(void);
extern u32 native_fn_02042b3c(u8 *state, Params *out);
extern void native_fn_0203cac8(u8 *a, u32 b);
extern void native_fn_0203caa4(u8 *a, u32 b);
extern void native_fn_0203cf9c(u32 a);
extern u32 native_fn_0205d6f4(u32 a);
extern u8 *native_fn_0207afec(u32 a);

extern u32 native_fn_ov001_021dba58(u32 a, u32 b);
extern u8 *native_fn_ov001_021d8b4c(u32 a, u32 b);
extern u8 *native_fn_ov001_021d8b78(u32 a);
extern void native_fn_ov001_021d95b0(u8 *a);
extern void native_fn_ov001_021e33c8(u32 a, u32 b, u32 c);
extern void native_fn_ov001_021e3408(u8 *a);
extern u32 native_fn_ov001_021d767c(void);
extern void native_fn_ov001_021eeb70(u16 a);
extern u32 native_fn_ov001_021eedbc(u32 a, u32 b, u32 c, u32 d, u32 e);
extern u32 native_fn_ov001_02216ac4(u32 a, u32 b, u32 c);
