typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed long s32;
typedef volatile u16 vu16;
typedef u32 REGType32;
typedef u64 REGType64;
typedef vu16 REGType16v;
static inline void CP_SetDivImm32_32_NS_ (u32 numer, u32 denom)
{
	*(REGType32 *)(0x04000000 + 0x290) = numer;
	*(REGType64 *)(0x04000000 + 0x298) = denom;
}
static inline void CP_SetDiv32_32 (u32 numer, u32 denom)
{
	(*( REGType16v *) (0x04000000 + 0x280)) = (0UL << 0) ;
	CP_SetDivImm32_32_NS_(numer, denom);
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
static inline s32 CP_GetDivResultImm32 (void)
{
	return (s32)(*(REGType32 *)(0x04000000 + 0x2a0) );
}
static inline s32 CP_GetDivResult32 (void)
{
	CP_WaitDiv();
	return CP_GetDivResultImm32();
}
s32 native_main_02002480(s32 a, s32 b);
s32 native_main_02002480 (s32 a, s32 b)
{
	((void) 0) ;
	((void) 0) ;
	CP_SetDiv32_32((u32)a, (u32)b);
	return CP_GetDivResult32();
}
