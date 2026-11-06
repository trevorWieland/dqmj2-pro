typedef unsigned short int u16;
typedef signed long s32;
typedef volatile u16 vu16;
typedef vu16 REGType16v;
        typedef int BOOL;
s32 native_main_02002be0(BOOL enable);
s32 native_main_02002be0 (BOOL enable)
{
	s32 rval = ((*( REGType16v *) (0x04000000 + 0x004)) & 0x0008 );
	if (enable) {
		(*( REGType16v *) (0x04000000 + 0x004)) |= 0x0008 ;
	} else {
		(*( REGType16v *) (0x04000000 + 0x004)) &= ~0x0008 ;
	}
	return rval;
}
