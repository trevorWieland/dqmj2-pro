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
extern u32 native_fn_02084f4c(u32);
extern u32 native_fn_02084f60(u32);
extern u32 native_fn_02088578(u8);
extern u8 native_data_ov000_02238514[];
extern u8 native_data_ov000_0223852b[];

typedef struct {u8 opaque[0x40];s32 value;} Field491_s32_0040;
typedef struct {u8 opaque[0x44];s32 value;} Field491_s32_0044;
typedef struct {u8 opaque[0x48];s32 value;} Field491_s32_0048;
typedef struct {u8 opaque[0x60];s32 value;} Field491_s32_0060;
typedef struct {void* value;} Field491_voidptr_0000;
typedef struct {u8 opaque[0x4];void* value;} Field491_voidptr_0004;
