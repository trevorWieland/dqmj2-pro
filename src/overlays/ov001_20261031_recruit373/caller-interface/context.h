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
extern void *native_fn_0202a634(void);
extern u32 native_fn_02041538(u32, u32, u32);
extern u32 native_fn_02044cdc();
extern u32 native_fn_02047ff0();
extern u32 native_fn_020491f8(u32);
extern u32 native_fn_02062850();
extern u8 *native_fn_02062a10(u32);
extern u32 native_fn_02062a50();
extern u32 native_fn_02062aa0();
extern int native_fn_02062e18(u32, void *);
extern u32 native_fn_02068f60(s8);
extern u32 native_fn_0206940c(void);
extern u32 native_fn_020698f4();
extern u32 native_fn_0206a04c(void);
extern u32 native_fn_0206a06c();
extern u32 native_fn_0206a0fc();
extern u32 native_fn_0206a49c(void);
extern u32 native_fn_0206bdc8(void);
extern u32 native_fn_0206be08(u32, u32);
extern u32 native_fn_0206be2c(void);
extern u32 native_fn_0206bf34(void);
extern u32 native_fn_0206bf44();
extern void *native_fn_0206c078(void);
extern u32 native_fn_0206c0b0(void);
extern u32 native_fn_0206c130(void);
extern u32 native_fn_0206dcd0(void *);
extern u32 native_fn_0206de1c();
extern u32 native_fn_0206de44(s8);
extern u32 native_fn_0206de64(s8);
extern u32 native_fn_0207e874();
extern void *native_fn_0207f3b0(void);
extern u32 native_fn_ov001_021dc2f8(u32);
extern u8 * native_fn_ov001_021fbe70(void);
extern u32 ov001_table_f0_entry_02202360();
extern void native_fn_ov001_02209b4c(void);
extern u32 native_fn_ov001_02209c34();
extern u32 native_fn_ov001_0220a3d8();
extern u32 native_fn_ov001_0220a3f0();
extern u32 native_fn_ov001_0220a408();
extern u32 native_fn_ov001_0220a97c(u32);
extern u32 native_fn_ov001_0220b21c(u32);
typedef struct {
    u8 unknown_0[0x14];
    s32 field_14;
    u32 field_18;
    u32 field_1c;
} Record_native_data_ov001_0223def8;
extern Record_native_data_ov001_0223def8 native_data_ov001_0223def8;
