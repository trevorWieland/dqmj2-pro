typedef unsigned long u32;
typedef unsigned long long int u64;
typedef signed long s32;
typedef signed long long int s64;
typedef u64 REGType64;
typedef s32 fx32;
typedef s64 fx64;
typedef s64 fx64c;
typedef union {
        struct {
            fx32 _00, _01, _02, _03;
            fx32 _10, _11, _12, _13;
            fx32 _20, _21, _22, _23;
            fx32 _30, _31, _32, _33;
        };
        fx32 m[4][4];
        fx32 a[16];
    } MtxFx44;
static fx32 FX_MulInline(fx32 v1, fx32 v2);
static fx32 FX_Mul32x64cInline(fx32 v32, fx64c v64c);
void native_main_02002210(fx32 fovySin, fx32 fovyCos, fx32 aspect, fx32 n, fx32 f, fx32 scaleW, MtxFx44 * mtx);
fx32 native_fn_0200235c(fx32 numer, fx32 denom);
static void FX_DivAsyncImm(fx32 numer, fx32 denom);
fx64c native_fn_020023a0(void);
fx32 native_fn_020023c4(void);
static void FX_InvAsyncImm(fx32 denom);
static fx64c FX_GetInvResultFx64c(void);
static inline fx32 FX32_CAST (s64 res)
    {
        ((void) 0) ;
        return (fx32)res;
    }
static inline fx32 FX_MulInline (fx32 v1, fx32 v2)
    {
        return FX32_CAST(((s64)(v1) * v2 + 0x800LL) >> 12 );
    }
static inline fx32 FX_Mul32x64cInline (fx32 v32, fx64c v64c)
    {
        fx64c tmp = v64c * v32 + 0x80000000LL;
        return FX32_CAST(tmp >> 32 );
    }
static inline void CP_SetDivImm64_32_NS_ (u64 numer, u32 denom)
{
	*(REGType64 *)(0x04000000 + 0x290) = numer;
	*(REGType64 *)(0x04000000 + 0x298) = denom;
}
static inline void CP_SetDivImm64_32 (u64 numer, u32 denom)
{
	CP_SetDivImm64_32_NS_(numer, denom);
}
static inline void FX_InvAsyncImm (fx32 denom)
{
	((void) 0) ;
	((void) 0) ;
	CP_SetDivImm64_32((u64)((fx32) 0x0000000000001000L) << 32, (u32)denom);
}
static inline fx64c FX_GetInvResultFx64c (void)
{
	return native_fn_020023a0();
}
static inline void FX_DivAsyncImm (fx32 numer, fx32 denom)
{
	((void) 0) ;
	((void) 0) ;
	CP_SetDivImm64_32((u64)numer << 32, (u32)denom);
}
