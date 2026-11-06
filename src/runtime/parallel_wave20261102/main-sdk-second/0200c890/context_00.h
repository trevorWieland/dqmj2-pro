typedef unsigned char u8;
typedef unsigned short int u16;
typedef unsigned long u32;
typedef int BOOL;
void native_fn_02008430();
void native_fn_02000950(void * bottom);
extern void native_fn_02008430(void);
void native_fn_02008d78(void * dest, u8 data, u32 size);
void native_fn_02007308(const void * startAddr, u32 nBytes);
typedef enum {
	MI_PROCESSOR_ARM9 = 0,
	MI_PROCESSOR_ARM7 = 1
} MIProcessor;
typedef struct {
	u32 offset;
	u32 length;
} CARDRomRegion;
typedef void (*FSOverlayInitFunc) (void);
typedef struct {
	u32 id;
	u8 * ram_address;
	u32 ram_size;
	u32 bss_size;
	FSOverlayInitFunc * sinit_init;
	FSOverlayInitFunc * sinit_init_end;
	u32 file_id;
	u32 compressed : 24;
	u32 flag : 8;
} FSOverlayInfoHeader;
typedef struct {
	FSOverlayInfoHeader header;
	MIProcessor target;
	CARDRomRegion file_pos;
} FSOverlayInfo;
void native_main_0200c890(FSOverlayInfo * p_ovi);
typedef struct {
	u16 length;
	u16 rssi;
	u16 bssid[3];
	u16 ssidLength;
	u8 ssid[32];
	u16 capaInfo;
	struct {
		u16 basic;
		u16 support;
	} rateSet;
	u16 beaconPeriod;
	u16 dtimPeriod;
	u16 channel;
	u16 cfpPeriod;
	u16 cfpMaxDuration;
} MBParentBssDesc;
typedef struct {
	u16 boot_type;
	MBParentBssDesc parent_bss_desc;
} MBParam;
extern u8 native_data_main_020e3300[];
extern u8 native_data_main_020e3300[];
u32 native_fn_0200c4fc (const FSOverlayInfo *p_ovi);
BOOL native_fn_0200c7fc (const u8 *spec_digest, void *src, int len);
static inline void MI_CpuClear8 (void * dest, u32 size)
{
	native_fn_02008d78(dest, 0, size);
}
static inline u32 FS_GetOverlayImageSize (const FSOverlayInfo * p_ovi)
{
	return (u32)(p_ovi->header.ram_size);
}
static inline void * FS_GetOverlayAddress (const FSOverlayInfo * p_ovi)
{
	return p_ovi->header.ram_address;
}
static inline const MBParam * MB_GetMultiBootParam (void)
{
	return (const MBParam *)(0x02000000 + 0x007ffc40) ;
}
static inline BOOL MB_IsMultiBootChild (void)
{
	return MB_GetMultiBootParam()->boot_type == 2 ;
}
