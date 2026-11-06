typedef signed int s32;
typedef unsigned int u32;
typedef unsigned short u16;
typedef signed short s16;
typedef signed long long s64;
typedef unsigned long long u64;
extern const s16 native_math_sincos_020d3fe0[8192];
extern u32 native_fn_02000dcc(void *,s32,s32);
extern u32 native_fn_02000de8(void *,s32,s32);
extern u32 native_fn_02000e04(void *,s32,s32);
void native_main_02027fe8(void *output,s32 angle) {
    u16 phase=(u16)((((u64)(s64)angle * 0xB60B60B60BULL) + 0x80000000000ULL) >> 44);
    u32 index=(phase >> 4) * 2;
    native_fn_02000dcc(output,native_math_sincos_020d3fe0[index],native_math_sincos_020d3fe0[index+1]);
}
void native_main_02028044(void *output,s32 angle) {
    u16 phase=(u16)((((u64)(s64)angle * 0xB60B60B60BULL) + 0x80000000000ULL) >> 44);
    u32 index=(phase >> 4) * 2;
    native_fn_02000de8(output,native_math_sincos_020d3fe0[index],native_math_sincos_020d3fe0[index+1]);
}
void native_main_020280a0(void *output,s32 angle) {
    u16 phase=(u16)((((u64)(s64)angle * 0xB60B60B60BULL) + 0x80000000000ULL) >> 44);
    u32 index=(phase >> 4) * 2;
    native_fn_02000e04(output,native_math_sincos_020d3fe0[index],native_math_sincos_020d3fe0[index+1]);
}
