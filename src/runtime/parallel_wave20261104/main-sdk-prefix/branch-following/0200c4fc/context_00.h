typedef unsigned char u8;
typedef unsigned long u32;
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
