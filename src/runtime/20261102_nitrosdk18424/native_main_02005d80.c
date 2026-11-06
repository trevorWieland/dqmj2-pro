typedef unsigned short int u16;
typedef unsigned long u32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
        typedef int BOOL;
        typedef u32 OSIrqMask;
static inline BOOL OS_DisableIrq (void)
{
	u16 prep = (*( REGType16v *) (0x04000000 + 0x208)) ;
	(*( REGType16v *) (0x04000000 + 0x208)) = (0UL << 0) ;
	return (BOOL)prep;
}
static inline BOOL OS_RestoreIrq (BOOL enable)
{
	u16 prep = (*( REGType16v *) (0x04000000 + 0x208)) ;
	(*( REGType16v *) (0x04000000 + 0x208)) = (u16)enable;
	return (BOOL)prep;
}
OSIrqMask native_main_02005d80(OSIrqMask intr);
extern const u16 (*ctrdgi_fl_maxtime);
OSIrqMask native_main_02005d80 (OSIrqMask intr)
{
    BOOL ime = OS_DisableIrq();
    OSIrqMask prep = (*( REGType32v *) (0x04000000 + 0x214)) ;
    (*( REGType32v *) (0x04000000 + 0x214)) = intr;
    (void)OS_RestoreIrq(ime);
    return prep;
}
