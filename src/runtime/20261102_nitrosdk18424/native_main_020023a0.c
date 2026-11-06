typedef unsigned short int u16;
    typedef unsigned long long int u64;
typedef signed long s32;
    typedef signed long long int s64;
typedef volatile u16 vu16;
typedef u64 REGType64;
typedef vu16 REGType16v;
typedef s64 fx64c;
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
fx64c native_main_020023a0(void);
fx64c native_main_020023a0 (void)
{
	return (fx64c)CP_GetDivResult64();
}
