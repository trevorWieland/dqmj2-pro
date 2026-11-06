typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
void * native_main_02003ea8(void);
static inline int getBGScreenOffset_ (void)
{
	return (int)(0x10000 * (((*( REGType32v *) (0x04000000 + 0x000)) & 0x38000000 ) >>
	                        27 ));
}
void *native_main_02003ea8 (void)
{
	int baseBlock = 0x800 * (((*( REGType16v *) (0x04000000 + 0x00a)) & 0x1f00 ) >>
	                         8 );
	return (void *)(0x06000000 + getBGScreenOffset_() + baseBlock);
}
