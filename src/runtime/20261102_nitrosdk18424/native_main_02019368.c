typedef unsigned short int u16;
typedef volatile u16 vu16;
typedef vu16 REGType16v;
typedef enum {
	MI_CTRDG_ROMCYCLE1_10 = 0,
	MI_CTRDG_ROMCYCLE1_8 = 1,
	MI_CTRDG_ROMCYCLE1_6 = 2,
	MI_CTRDG_ROMCYCLE1_18 = 3
} MICartridgeRomCycle1st;
typedef enum {
	MI_CTRDG_ROMCYCLE2_6 = 0,
	MI_CTRDG_ROMCYCLE2_4 = 1
} MICartridgeRomCycle2nd;
static inline void MI_SetCartridgeRomCycle1st (MICartridgeRomCycle1st c1)
{
	((void) 0) ;
	(*( REGType16v *) (0x04000000 + 0x204)) =
		(u16)(((*( REGType16v *) (0x04000000 + 0x204)) & ~0x000c ) |
		      (c1 << 2 ));
}
static inline void MI_SetCartridgeRomCycle2nd (MICartridgeRomCycle2nd c2)
{
	((void) 0) ;
	(*( REGType16v *) (0x04000000 + 0x204)) =
		(u16)(((*( REGType16v *) (0x04000000 + 0x204)) & ~0x0010 ) |
		      (c2 << 4 ));
}
typedef struct CTRDGRomCycle {
	MICartridgeRomCycle1st c1;
	MICartridgeRomCycle2nd c2;
} CTRDGRomCycle;
void native_main_02019368(CTRDGRomCycle * r);
extern const u16 (*ctrdgi_fl_maxtime);
void native_main_02019368 (CTRDGRomCycle *r)
{
	MI_SetCartridgeRomCycle1st(r->c1);
	MI_SetCartridgeRomCycle2nd(r->c2);
}
