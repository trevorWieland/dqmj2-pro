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
extern u32 ov001_record_is_active_021db8d0(u8 *);
extern u32 native_fn_ov001_021e29e8();
extern u32 ov001_any_active_slot_compare_022187dc();
extern u32 native_fn_ov001_02218dbc();

typedef struct {u8 opaque[0x4];s32 value;} Field491_s32_0004;
typedef struct {u8 opaque[0x23c];s8 value;} Field491_s8_023c;
typedef struct {u8 opaque[0x323];u8 value;} Field491_u8_0323;
typedef struct {u8 opaque[0x35e];u8 value;} Field491_u8_035e;
