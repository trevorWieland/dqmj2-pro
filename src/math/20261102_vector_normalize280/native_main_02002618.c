typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed int s32;
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
void native_main_02002618(const VecFx32 * pSrc, VecFx32 * pDst);
static inline void CP_SetDivImm64_64_NS_ (u64 numer, u64 denom)
{
	*(REGType64 *)(0x04000000 + 0x290) = numer;
	*(REGType64 *)(0x04000000 + 0x298) = denom;
}
static inline void CP_SetDiv64_64 (u64 numer, u64 denom)
{
	(*( REGType16v *) (0x04000000 + 0x280)) = (2UL << 0) ;
	CP_SetDivImm64_64_NS_(numer, denom);
}
static inline s32 CP_IsDivBusy (void)
{
	return ((*( REGType16v *) (0x04000000 + 0x280)) & 0x8000 );
}
static inline void CP_WaitDiv (void)
{
	while (CP_IsDivBusy()) {
	}
}
static inline s64 CP_GetDivResultImm64 (void)
{
	return (s64)(*(REGType64 *)(0x04000000 + 0x2a0) );
}
static inline s64 CP_GetDivResult64 (void)
{
	CP_WaitDiv();
	return CP_GetDivResultImm64();
}
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
void native_main_02002618 (const VecFx32 *pSrc, VecFx32 *pDst)
{
	fx64 t;
	s32 sqrt;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	t  = (fx64)pSrc->x * pSrc->x;
	t += (fx64)pSrc->y * pSrc->y;
	t += (fx64)pSrc->z * pSrc->z;
	((void) 0) ;
	((void) 0) ;
	CP_SetDiv64_64(1LL << (12 + 12 + 32 ), (u64)t);
	CP_SetSqrt64((u64)(t << 2));
	sqrt = (s32)CP_GetSqrtResult32();
    t = CP_GetDivResult64();
	t = t * sqrt;
	pDst->x = (fx32)((t * pSrc->x + (1LL << (32 + 12 ))) >> (32 + 12 + 1));
	pDst->y = (fx32)((t * pSrc->y + (1LL << (32 + 12 ))) >> (32 + 12 + 1));
	pDst->z = (fx32)((t * pSrc->z + (1LL << (32 + 12 ))) >> (32 + 12 + 1));
}

typedef char checked_u32_width[(sizeof(u32)==4)?1:-1];
