typedef unsigned long u32;
extern u32 native_data_main_020dcb44;
void native_main_020048f4(const void * pSrc, u32 offset, u32 szByte);
void native_fn_0200854c(u32 dmaNo, const void * src, void * dest, u32 size);
void native_fn_02008bf8(const void * srcp, void * destp, u32 size);
static inline void MI_CpuCopy16 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008bf8(src, dest, size);
}
static void GXi_DmaCopy16(u32 dmaNo, const void * src, void * dest, u32 size);
static inline void GXi_DmaCopy16 (u32 dmaNo, const void * src, void * dest, u32 size)
{
	if (dmaNo != ((u32) ~0) && size > 28 ) {
		native_fn_0200854c(dmaNo, src, dest, size);
	} else {
		MI_CpuCopy16(src, dest, size);
	}
}
void native_main_020048f4 (const void *pSrc, u32 offset, u32 szByte)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	GXi_DmaCopy16(native_data_main_020dcb44, pSrc, (void *)(0x05000400 + offset), szByte);
}
