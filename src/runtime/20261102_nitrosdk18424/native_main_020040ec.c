typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
void * native_main_020040ec(void);
static inline int getBGCharOffset_ (void)
{
	return (int)(0x10000 * (((*( REGType32v *) (0x04000000 + 0x000)) & 0x07000000 ) >>
	                        24 ));
}
void * native_main_020040ec (void)
{
	int baseBlock = 0x4000 * (((*( REGType16v *) (0x04000000 + 0x008)) & 0x003c ) >> 2 );
	return (void *)(0x06000000 + getBGCharOffset_() + baseBlock);
}
