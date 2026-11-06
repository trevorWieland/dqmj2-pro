typedef unsigned short int u16;
typedef unsigned long u32;
typedef signed long s32;
typedef volatile u16 vu16;
typedef volatile u32 vu32;
typedef vu16 REGType16v;
typedef vu32 REGType32v;
typedef int BOOL;
void native_fn_02008430();
void native_fn_0200845c(u32 dmaNo, void * dest, u32 data, u32 size);
void native_fn_02008c14(u32 data, void * destp, u32 size);
extern void native_fn_02008430(void);
s32 native_fn_020060e4(void);
typedef enum {
	GX_POWER_OFF        = 0,
	GX_POWER_2D_MAIN    = 1 << 1 ,
	GX_POWER_2D_SUB     = 1 << 9 ,
	GX_POWER_RE         = 1 << 2 ,
	GX_POWER_GE         = 1 << 3 ,
	GX_POWER_2D         = GX_POWER_2D_MAIN | GX_POWER_2D_SUB,
	GX_POWER_3D         = GX_POWER_RE | GX_POWER_GE,
	GX_POWER_ALL        = GX_POWER_2D | GX_POWER_3D
} GXPower;
static void GX_SetPower(int gxbit_power);
static void GXi_PowerLCD(BOOL enable);
void native_main_02002a94(void);
void native_fn_02002d44(void);
typedef struct {
u16 field_0000;
vu16 field_0002;
} NativeStorage_020e3300;
extern NativeStorage_020e3300 native_data_main_020e3300;
typedef struct {
u16 field_0000;
unsigned char padding_0002[2];
u32 field_0004;
} NativeStorage_020dcb40;
extern NativeStorage_020dcb40 native_data_main_020dcb40;
static inline void MI_CpuFill32 (void * dest, u32 data, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c14(data, dest, size);
}
static inline void GX_SetPower (int gxbit_power)
{
	((void) 0) ;
	(*( REGType16v *) (0x04000000 + 0x304)) = (u16)(((*( REGType16v *) (0x04000000 + 0x304)) & ~GX_POWER_ALL) | gxbit_power);
}
static inline void GXi_PowerLCD (BOOL enable)
{
	if (enable) {
		(*( REGType16v *) (0x04000000 + 0x304)) |= 0x0001 ;
	} else {
		(*( REGType16v *) (0x04000000 + 0x304)) &= ~0x0001 ;
	}
}
