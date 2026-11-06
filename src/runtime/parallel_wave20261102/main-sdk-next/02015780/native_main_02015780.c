#include "context_00.h"
BOOL native_main_02015780 (FSFile * file, void * buf, u32 len)
{
	BOOL ret = 0 ;
	((void) 0) ;
	if (len >= (0x160) + 4) {
		BOOL is_own_binary = 0 ;
		u32 rest = len;
		u8 * dst = (u8 *)buf;
		u32 bak_pos;
		FSFile own_bin[1];
		u32 own_size;
		RomHeader * p_rom;
		MBiCacheList * p_cache = ((void *)0) ;
		u32 * p_map = ((void *)0) ;
		p_rom = (RomHeader *) dst;
		dst += (0x160) , rest -= (0x160) ;
		if (file) {
			bak_pos = FS_GetPosition(file);
			if (native_fn_0200c180(file, p_rom, (0x160) ) < (0x160) )
				rest = 0;
			own_size = p_rom->own_size;
			if (!own_size)
				own_size = 16 * 1024 * 1024;
		} else {
			const RomHeader * mem_rom = (RomHeader *) (0x02000000 + 0x007ffe00) ;
			own_size = mem_rom->own_size;
			if (!own_size)
				own_size = 16 * 1024 * 1024;
			is_own_binary = 1 ;
			native_fn_0200bd04(own_bin);
			(void)native_fn_0200bf2c(own_bin, native_fn_0200b6d4(native_data_main_020dce90, 3), 0, (u32)(own_size + (136) ), (u32) ~0);
			file = own_bin;
			bak_pos = FS_GetPosition(file);
			native_fn_02008e0c(mem_rom, p_rom, (0x160) );
			*(u32 *)((u32)p_rom + 0x60) |= 0x00406000;
		}
		if (rest >= (136) ) {
			(void)native_fn_0200c190(file, (int)(bak_pos + own_size), FS_SEEK_SET);
			(void)native_fn_0200c180(file, dst, (136) );
			dst += (136) , rest -= (136) ;
		} else {
			rest = 0;
		}
		if (rest >= sizeof(MBiCacheList)) {
			p_cache = (MBiCacheList *) dst;
			native_fn_020189e8(p_cache);
			dst += sizeof(MBiCacheList), rest -= sizeof(MBiCacheList);
			native_fn_020189fc(p_cache, 0, (0x160) , p_rom, 3 );
			{
				FSArchive * p_arc = FS_GetAttachedArchive(file);
				int i = 0;
				while ((i < FS_ARCHIVE_NAME_LEN_MAX) && p_arc->name.ptr[i])
					++i;
				native_fn_02008e0c(p_arc->name.ptr, p_cache->arc_name, (u32)i);
				p_cache->arc_name_len = (u32)i;
				p_cache->arc_pointer = p_arc;
			}
		} else {
			rest = 0;
		}
		if (rest >= sizeof(u32) * 4) {
			p_map = (u32 *)dst;
			p_map[0] = 0;
			p_map[1] = FS_GetFileImageTop(file) + bak_pos + p_rom->main_rom_offset;
			p_map[2] = FS_GetFileImageTop(file) + bak_pos + p_rom->sub_rom_offset;
			dst += sizeof(u32) * 4, rest -= sizeof(u32) * 4;
		} else {
			rest = 0;
		}
		if (rest >= p_rom->main_size + p_rom->sub_size) {
			const u32 base = FS_GetFileImageTop(file);
			(void)native_fn_0200c190(file, (int)(p_map[1] - base), FS_SEEK_SET);
			(void)native_fn_0200c180(file, dst, (int)p_rom->main_size);
			native_fn_020189fc(p_cache, p_map[1], p_rom->main_size, dst, 3 );
			dst += p_rom->main_size, rest -= p_rom->main_size;
			(void)native_fn_0200c190(file, (int)(p_map[2] - base), FS_SEEK_SET);
			(void)native_fn_0200c180(file, dst, (int)p_rom->sub_size);
			native_fn_020189fc(p_cache, p_map[2], p_rom->sub_size, dst, 3 );
			dst += p_rom->sub_size, rest -= p_rom->sub_size;
			ret = 1 ;
		} else if (rest >= (17 * 1024) * 3)   {
			const u32 base = FS_GetFileImageTop(file);
			u32 offset = p_map[1];
			(void)native_fn_0200c190(file, (int)(offset - base), FS_SEEK_SET);
			(void)native_fn_0200c180(file, dst, (17 * 1024) );
			native_fn_020189fc(p_cache, offset, (17 * 1024) , dst, 3 );
			dst += (17 * 1024) , rest -= (17 * 1024) ;
			offset += (17 * 1024) ;
			(void)native_fn_0200c190(file, (int)(offset - base), FS_SEEK_SET);
			(void)native_fn_0200c180(file, dst, (17 * 1024) );
			native_fn_020189fc(p_cache, offset, (17 * 1024) , dst, 2 );
			dst += (17 * 1024) , rest -= (17 * 1024) ;
			offset += (17 * 1024) ;
			(void)native_fn_0200c190(file, (int)(offset - base), FS_SEEK_SET);
			(void)native_fn_0200c180(file, dst, (17 * 1024) );
			native_fn_020189fc(p_cache, offset, (17 * 1024) , dst, 2 );
			dst += (17 * 1024) , rest -= (17 * 1024) ;
			ret = 1 ;
		}
		(void)native_fn_0200c190(file, (int)bak_pos, FS_SEEK_SET);
		if (is_own_binary) {
			(void)native_fn_0200c02c(own_bin);
			if (ret) {
				const CARDRomRegion * p_header = native_data_main_020dce8c.field_0000;
				MBiSegmentHeaderInfo info;
				info.rom_src = p_rom->main_rom_offset;
				info.mem_src = (u32)((u32)p_rom->main_ram_address - p_rom->main_rom_offset);
				info.mem_dst = (u32)((u32)p_cache->list[1].ptr - p_rom->main_rom_offset);
				info.len = len;
				native_fn_02015bf8(&info, 0x4000 , 0x8000 , 1 );
				for (; p_header->length != 0; ++p_header) {
					native_fn_02015bf8(&info,
					                      p_header->offset,
					                      (u32)(p_header->offset + p_header->length), 0 );
				}
				{
					extern u32 native_data_main_02000a74[1];
					u8 * dst = (u8 *)p_cache->list[1].ptr;
					dst += ((u32) & native_data_main_02000a74 - (u32)p_rom->main_ram_address);
					*(u32 *)dst = 0xE12FFF1E;
				}
			}
		}
		if (ret) {
			native_fn_02007308(buf, len);
		}
	}
	return ret;
}
