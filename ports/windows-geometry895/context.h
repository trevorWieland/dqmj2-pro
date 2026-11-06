typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;
typedef char pointer_width[(sizeof(void *) == 4) ? 1 : -1];
typedef char word_width[(sizeof(u32) == 4) ? 1 : -1];
extern u8 portable_global_state[0x7A0];
#define iRam021dc370 ((s32) portable_global_state)
extern u32 native_fn_0200235c(u32 numerator, s32 denominator);
extern u32 native_fn_ov000_021dbbb8(void *context, void *point);
extern u32 native_fn_ov000_021da57c(void *context, s32 index, void *triangle, u32 mesh);
