typedef unsigned char u8;
typedef unsigned long u32;
        typedef int BOOL;
typedef enum MbSegmentType {
	MB_SEG_ARM9STATIC = 0,
	MB_SEG_ARM7STATIC,
	MB_SEG_ROMHEADER
} MbSegmentType;
extern const MbSegmentType native_data_main_020d8ce0[(3) ];
BOOL native_fn_0201626c(u8 segment_no, u32 address, u32 size);
const MbSegmentType native_data_main_020d8ce0[(3) ] = {
	MB_SEG_ROMHEADER,
	MB_SEG_ARM9STATIC,
	MB_SEG_ARM7STATIC,
};
BOOL native_main_02016318(u8 segment_no, u32 address, u32 size);
BOOL native_fn_0201626c (u8 segment_no, u32 address, u32 size);
BOOL native_main_02016318 (u8 segment_no, u32 address, u32 size)
{
	MbSegmentType seg_type;
	((void) 0) ;
	seg_type = native_data_main_020d8ce0[segment_no];
	switch (seg_type) {
	case MB_SEG_ROMHEADER:
	case MB_SEG_ARM9STATIC:
		return native_fn_0201626c(segment_no, address, size);
	case MB_SEG_ARM7STATIC:
		if (address >= (0x02000000) && address < (0x02000000 + 0x003fe800) ) {
			u32 end_adr = address + size;
			if ((0x02000000 + 0x00300000) > address
			    && (0x02000000 + 0x00300000) < end_adr) {
				return 0 ;
			} else if (end_adr <= ((0x02000000 + 0x002c0000) + ((0x02000000 + 0x00300000) - (0x02000000 + 0x002c0000))) )   {
				return 1 ;
			} else if (end_adr < (0x02000000 + 0x003fe800) && size <= ((0x02000000 + 0x00300000) - (0x02000000 + 0x002c0000)) )   {
				return 1 ;
			} else {
				return 0 ;
			}
		} else if (address >= 0x037f8000 && address < 0x037f8000 + (0x18000 - 0x1000) )        {
			u32 end_adr = address + size;
			if (end_adr <= (0x037f8000 + (0x18000 - 0x1000) )) {
				return 1 ;
			} else {
				return 0 ;
			}
		}
		break;
	default:
		return 0 ;
	}
	return 0 ;
}
