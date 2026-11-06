typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed long s32;
    typedef signed long long int s64;
typedef volatile u16 vu16;
typedef u32 REGType32;
typedef u64 REGType64;
typedef vu16 REGType16v;
typedef s32 fx32;
typedef s64 fx64;
typedef struct {
    fx32 x;
    fx32 y;
    fx32 z;
} VecFx32;
fx32 native_main_020025b8(const VecFx32 * v);
static inline void CP_SetSqrtImm64_NS_ (u64 param)
{
	*((REGType64 *)(0x04000000 + 0x2b8) ) = param;
}
static inline void CP_SetSqrt64 (u64 param)
{
	(*( REGType16v *) (0x04000000 + 0x2b0)) = (1UL << 0) ;
	CP_SetSqrtImm64_NS_(param);
}
static inline s32 CP_IsSqrtBusy (void)
{
	return ((*( REGType16v *) (0x04000000 + 0x2b0)) & 0x8000 );
}
static inline void CP_WaitSqrt (void)
{
	while (CP_IsSqrtBusy()) {
	}
}
static inline u32 CP_GetSqrtResultImm32 (void)
{
	return (u32)(*((REGType32 *)(0x04000000 + 0x2b4) ));
}
static inline u32 CP_GetSqrtResult32 (void)
{
	CP_WaitSqrt();
	return CP_GetSqrtResultImm32();
}
fx32 native_main_020025b8 (const VecFx32 *pSrc)
{
	fx64 t;
	fx32 rval;
	((void) 0) ;
	((void) 0) ;
	t  = (fx64)pSrc->x * pSrc->x;
	t += (fx64)pSrc->y * pSrc->y;
	t += (fx64)pSrc->z * pSrc->z;
	t <<= 2;
	CP_SetSqrt64((u64)t);
	rval = ((fx32)CP_GetSqrtResult32() + 1) >> 1;
	return rval;
}
