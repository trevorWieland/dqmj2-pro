typedef unsigned char u8;
typedef unsigned long u32;
    typedef u32 OSIntrMode;
    extern OSIntrMode native_fn_02007ff4(void);
    extern OSIntrMode native_fn_02008008(OSIntrMode state);
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
static inline u32 FS_GetOverlayTotalSize (const FSOverlayInfo * p_ovi)
{
	return (u32)(p_ovi->header.ram_size + p_ovi->header.bss_size);
}
static inline void * FS_GetOverlayAddress (const FSOverlayInfo * p_ovi)
{
	return p_ovi->header.ram_address;
}
void native_main_0200c984(FSOverlayInfo * p_ovi);
typedef void (*MWI_DESTRUCTOR_FUNC) (void *);
typedef struct MWiDestructorChain {
	struct MWiDestructorChain * next;
	MWI_DESTRUCTOR_FUNC dtor;
	void * obj;
} MWiDestructorChain;
extern MWiDestructorChain * native_data_main_020ec9b4;
void native_main_0200c984 (FSOverlayInfo *p_ovi)
{
	for (;;) {
		MWiDestructorChain *head = ((void *)0) , *tail = ((void *)0) ;
		const u32 region_top = (u32)FS_GetOverlayAddress(p_ovi);
		const u32 region_bottom = region_top + FS_GetOverlayTotalSize(p_ovi);
		{
			OSIntrMode bak_psr = native_fn_02007ff4();
			MWiDestructorChain *prev = ((void *)0) ;
			MWiDestructorChain *base = native_data_main_020ec9b4;
			MWiDestructorChain *p = base;
			while (p) {
				MWiDestructorChain *next = p->next;
				const u32 dtor = (u32)p->dtor;
				const u32 obj = (u32)p->obj;
				if (((obj == 0) && (dtor >= region_top) && (dtor < region_bottom)) ||
				    ((obj >= region_top) && (obj < region_bottom))) {
					if (!tail) {
						head = p;
					} else {
						tail->next = p;
					}
					if (base == p) {
						base = native_data_main_020ec9b4 = next;
					}
					tail = p, p->next = ((void *)0) ;
					if (prev) {
						prev->next = next;
					}
				} else {
					prev = p;
				}
				p = next;
			}
			(void)native_fn_02008008(bak_psr);
		}
		if (!head) {
			break;
		}
		do {
			MWiDestructorChain *next = head->next;
			if (head->dtor) {
				(*head->dtor)(head->obj);
			}
			head = next;
		} while (head);
	}
}
