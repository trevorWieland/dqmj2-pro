/* Shared declarations for the ov001 pass-4 packet (p11). */
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

/* overlay data blocks referenced through literal pools */
extern u8 native_data_ov001_0222e188[];
extern u8 native_data_ov001_0222e374[];
extern u8 native_data_ov001_0222e38c[];
extern u8 native_data_ov001_0222e398[];
extern u8 native_data_ov001_0222e44c[];
extern u8 native_data_ov001_0222e47c[];
extern u8 native_data_ov001_0222e4a0[];
extern u8 native_data_ov001_0222e4ac[];
extern u8 native_data_ov001_0222e4d0[];
extern u8 native_data_ov001_0222e4e8[];
extern u8 native_data_ov001_0222e500[];
extern u8 native_data_ov001_0222e524[];
extern u8 native_data_ov001_0222e68c[];
extern u8 native_data_ov001_0222e698[];
extern u8 native_data_ov001_0222e6a4[];
extern u8 native_data_ov001_0222e6b0[];
extern u8 native_data_ov001_0222e704[];
extern u8 native_data_ov001_0222e71c[];
extern u8 native_data_ov001_0222e734[];
extern u8 native_data_ov001_0222e740[];
extern u8 native_data_ov001_0222e74c[];
extern u8 native_data_ov001_0222e770[];
extern u8 native_data_ov001_0222e77c[];
extern u8 native_data_ov001_0222e788[];
extern u8 native_data_ov001_0222e794[];
extern u8 native_data_ov001_0222e7ac[];
extern u8 native_data_ov001_0222e7c4[];
extern u8 native_data_ov001_0222e7d0[];
extern u8 native_data_ov001_0222e7dc[];
extern u8 native_data_ov001_0222e7f4[];
extern u8 native_data_ov001_0222e80c[];
extern u8 native_data_ov001_0222e818[];
extern u8 native_data_ov001_0222e8c0[];

/* overlay and main call targets */
extern s32 native_fn_0207afec(s32 value);
extern s32 native_fn_ov001_021db8d0(u8 *entry);
extern s32 native_fn_ov001_02218524(u8 *entry, s32 flag);
extern void native_fn_ov001_02223fe8(u32 *block, u8 *entry);
extern void native_fn_ov001_02224050(void *local);
extern void native_fn_ov001_02224570(void *local, u8 *entry, s32 value);
extern void native_fn_ov001_0222463c(void *local, u8 *entry, s32 value);
extern void native_fn_ov001_02225bac(void *local, u8 *entry, s32 value);
extern void native_fn_ov001_02225d6c(void *local, u8 *entry, s32 value);
extern s32 native_fn_ov001_02226bdc(void *local, void *record, s32 command);
extern s32 native_fn_ov001_02226cb0(void *local);
