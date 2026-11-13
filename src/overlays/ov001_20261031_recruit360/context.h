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
extern u32 native_fn_0202a498();
extern u32 native_fn_0203cc2c(u32, u32);
extern u32 native_fn_02041538(u32, u32, u32);
extern u32 native_fn_0204518c(void *, u32, u32);
extern u32 native_fn_02045490();
extern void native_fn_02045680(s32);
extern u32 native_fn_02045994(u32, u32, s32, u32);
extern u8 *native_fn_02062a10(u32);
extern u32 native_fn_02062aa0();
extern u32 native_fn_02062ad0();
extern u32 native_fn_02068ae8();
extern u32 native_fn_02068eb8(u8, s8, s8, s8);
extern u32 native_fn_0206be08(u32, u32);
extern u32 native_fn_0206dcd0(void *);
extern u32 native_fn_0206de44(s8);
extern u32 native_fn_0207e720(void *);
extern u8 * native_fn_ov001_021fbe70(void);
extern u32 ov001_table_f0_entry_02202360();
extern u32 native_fn_ov001_0220a5e0();
extern u32 native_fn_ov001_0220a6cc();
extern u32 native_fn_ov001_0220aaa0();
extern u32 native_fn_ov001_0220aab8();
extern u32 native_fn_ov001_0220ad70(u32);
extern u32 native_fn_ov001_0220af00();
extern u32 native_fn_ov001_0220af68(u32);
extern u32 native_fn_ov001_0220afe4();
extern u32 native_fn_ov001_0220b0f0();
typedef struct {
    u16 field_0;
    u16 field_2;
} Record_native_data_ov001_0222e0e4;
extern Record_native_data_ov001_0222e0e4 native_data_ov001_0222e0e4;
extern u8 native_data_ov001_0222f0b0[];
typedef struct {
    u8 unknown_0[0x6];
    s8 field_6;
    u8 unknown_7[0xd];
    s32 field_14;
    s32 field_18;
    u32 field_1c;
    u8 unknown_20[0x10];
    s32 field_30;
} Record_native_data_ov001_0223def8;
extern Record_native_data_ov001_0223def8 native_data_ov001_0223def8;
extern u8 native_data_ov001_0223df1c[];

typedef struct {u8 kind; s16 species; u8 variant; u8 raw; const u8 *name; u8 length; u8 last;} Descriptor356;
