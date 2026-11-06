typedef unsigned short int u16;

typedef unsigned long u32;

typedef volatile u16 vu16;

typedef vu16 REGType16v;

typedef int BOOL;

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

extern const u16 (*ctrdgi_fl_maxtime);

void WaitLoop_ClrAid(void);
