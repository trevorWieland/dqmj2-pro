typedef unsigned long u32;
extern u32 native_data_main_020dcb44;
void native_main_02004aa8(const void * pSrc, u32 offset, u32 szByte);
static void * G2_GetOBJCharPtr(void);
static inline void * G2_GetOBJCharPtr (void)
{
	return (void *)0x06400000 ;
}
void native_fn_020084dc(u32 dmaNo, const void * src, void * dest, u32 size);
void native_fn_02008c28(const void * srcp, void * destp, u32 size);
static inline void MI_CpuCopy32 (const void * src, void * dest, u32 size)
{
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	native_fn_02008c28(src, dest, size);
}
    static inline void GX_RegionCheck_OBJ (u32, u32)
    {
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
void native_main_02004aa8 (const void *pSrc, u32 offset, u32 szByte)
{
	u32 ptr;
	((void) 0) ;
	((void) 0) ;
	((void) 0) ;
	ptr = (u32)G2_GetOBJCharPtr();
	GX_RegionCheck_OBJ(ptr + offset, ptr + offset + szByte);
	GXi_DmaCopy32(native_data_main_020dcb44, pSrc, (void *)(ptr + offset), szByte);
}
