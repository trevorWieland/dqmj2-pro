typedef unsigned long u32;
extern u32 native_data_main_020dcb44;
void native_main_020053c0(const void * pSrc, u32 destSlotAddr, u32 szByte);
typedef void (*MIDmaCallback) (void *);
void native_fn_0200867c(u32 dmaNo, const void * src, void * dest, u32 size, MIDmaCallback callback, void * arg);
void native_fn_02008c28(const void * srcp, void * destp, u32 size);
static inline void MI_CpuCopy32 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c28(src, dest, size);
}
static void GXi_DmaCopy32Async(u32 dmaNo, const void * src, void * dest, u32 size, MIDmaCallback callback, void * arg);
static inline void GXi_DmaCopy32Async (u32 dmaNo, const void * src, void * dest, u32 size,
                                       MIDmaCallback callback, void * arg)
{
	if (dmaNo != ((u32) ~0) ) {
		native_fn_0200867c(dmaNo, src, dest, size, callback, arg);
	} else {
		MI_CpuCopy32(src, dest, size);
	}
}
void native_main_020053c0 (const void *pSrc, u32 destSlotAddr, u32 szByte)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0)	              ;
	GXi_DmaCopy32Async(native_data_main_020dcb44,
	                   pSrc, (void *)(((((((((0x06800000) + 0x20000) + 0x20000) + 0x20000) + 0x20000) + 0x10000) + 0x4000) + 0x4000) + destSlotAddr), szByte, ((void *)0) , ((void *)0) );
}
