typedef unsigned long u32;
typedef signed long s32;
typedef volatile u32 vu32;
typedef vu32 REGType32v;
int native_main_020047ac(s32 * level);
int native_main_020047ac (s32 *level)
{
	((void) 0) ;
	if ((*( REGType32v *) (0x04000000 + 0x600)) & 0x00004000 ) {
		return -1;
	} else {
		*level = (s32)(((*( REGType32v *) (0x04000000 + 0x600)) & 0x00001f00 ) >> 8 );
		return 0;
	}
}
