typedef unsigned short int u16;
typedef unsigned long u32;
    typedef unsigned long long int u64;
typedef signed long s32;
typedef volatile u16 vu16;
typedef u64 REGType64;
typedef vu16 REGType16v;
typedef s32 fx32;
static inline void CP_SetDivImm64_32_NS_ (u64 numer, u32 denom)
{
	*(REGType64 *)(0x04000000 + 0x290) = numer;
	*(REGType64 *)(0x04000000 + 0x298) = denom;
}
static inline void CP_SetDiv64_32 (u64 numer, u32 denom)
{
	(*( REGType16v *) (0x04000000 + 0x280)) = (1UL << 0) ;
	CP_SetDivImm64_32_NS_(numer, denom);
}
void native_main_020023fc(fx32 denom);
void native_main_020023fc (fx32 denom)
{
	((void) 0) ;
	((void) 0) ;
	CP_SetDiv64_32((u64)((fx32) 0x0000000000001000L) << 32, (u32)denom);
}
