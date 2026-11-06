typedef unsigned long u32;
extern u32 native_data_main_020dcb44;
void native_main_020049fc(const void * pSrc, u32 offset, u32 szByte);
void native_fn_020084dc(u32 dmaNo, const void * src, void * dest, u32 size);
void native_fn_02008c28(const void * srcp, void * destp, u32 size);
static inline void MI_CpuCopy32 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c28(src, dest, size);
}
static void GXi_DmaCopy32(u32 dmaNo, const void * src, void * dest, u32 size);
static inline void GXi_DmaCopy32 (u32 dmaNo, const void * src, void * dest, u32 size)
{
	if (dmaNo != ((u32) ~0) && size > 48 ) {
		native_fn_020084dc(dmaNo, src, dest, size);
	} else {
		MI_CpuCopy32(src, dest, size);
	}
}
void native_main_020049fc (const void *pSrc, u32 offset, u32 szByte)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	GXi_DmaCopy32(native_data_main_020dcb44, pSrc, (void *)(0x07000000 + offset), szByte);
}
