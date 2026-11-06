#include "context_00.h"
FSResult native_main_0200ad10 (FSFile *p_file)
{
	FSArchive *const p_arc = p_file->arc;
	FSGetPathInfo *p_info = &p_file->arg.getpath;
	FSDirEntry entry;
	FSFile tmp;
	u32 dir_id;
	u32 file_id;
	u32 id;
	u32 len;
	enum {
        INVALID_ID = 0x10000
    };
	native_fn_0200bd04(&tmp);
	tmp.arc = p_file->arc;
	if (FS_IsDir(p_file)) {
		dir_id = p_file->prop.dir.pos.own_id;
		file_id = INVALID_ID;
	} else {
		file_id = p_file->prop.file.own_id;
		if (p_info->total_len != 0) {
			dir_id = p_info->dir_id;
		} else {
			u32 pos = 0;
			u32 num_dir = 0;
			dir_id = INVALID_ID;
			do {
				native_fn_0200a8dc(&tmp, pos);
				if (!pos)
					num_dir = tmp.prop.dir.parent;
				tmp.arg.readdir.p_entry = &entry;
				tmp.arg.readdir.skip_string = 1 ;
				while (native_fn_0200a63c(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
					if (!entry.is_directory && (entry.file_id.file_id == file_id)) {
						dir_id = tmp.prop.dir.pos.own_id;
						break;
					}
				}
			} while ((dir_id == INVALID_ID) && (++pos < num_dir));
		}
	}
	if (dir_id == INVALID_ID) {
		p_info->total_len = 0;
		return FS_RESULT_FAILURE;
	}
	if (p_info->total_len == 0) {
		len = 0;
		if (p_arc->name.pack <= 0x000000FF)
			len += 1;
		else if (p_arc->name.pack <= 0x0000FF00)
			len += 2;
		else
			len += 3;
		len += 1 + 1;
		if (file_id != INVALID_ID)
			len += entry.name_len;
		id = dir_id;
		if (id != 0) {
			native_fn_0200a8dc(&tmp, id);
			do {
				native_fn_0200a8dc(&tmp, tmp.prop.dir.parent);
				tmp.arg.readdir.p_entry = &entry;
				tmp.arg.readdir.skip_string = 1 ;
				while (native_fn_0200a63c(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
					if (entry.is_directory && (entry.dir_id.own_id == id)) {
						len += entry.name_len + 1;
						break;
					}
				}
				id = tmp.prop.dir.pos.own_id;
			} while (id != 0);
		}
		p_info->total_len = (u16)(len + 1);
		p_info->dir_id = (u16)dir_id;
	}
	if (!p_info->buf)
		return FS_RESULT_SUCCESS;
	if (p_info->buf_len < p_info->total_len)
		return FS_RESULT_FAILURE;
	else {
		u8 *dst = p_info->buf;
		u32 total = p_info->total_len;
		u32 pos = 0;
		if (p_arc->name.pack <= 0x000000FF)
			len = 1;
		else if (p_arc->name.pack <= 0x0000FF00)
			len = 2;
		else
			len = 3;
		native_fn_02008e0c(p_arc->name.ptr, dst + pos, len);
		pos += len;
		native_fn_02008e0c(native_data_main_020dcb5c, dst + pos, 2);
		pos += 2;
		id = dir_id;
		native_fn_0200a8dc(&tmp, id);
		if (file_id != INVALID_ID) {
			tmp.arg.readdir.p_entry = &entry;
			tmp.arg.readdir.skip_string = 0 ;
			while (native_fn_0200a63c(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
				if (!entry.is_directory && (entry.file_id.file_id == file_id))
					break;
			}
			len = entry.name_len + 1;
			native_fn_02008e0c(entry.name, dst + total - len, len);
			total -= len;
		} else {
			MI_WriteByte(dst + total - 1, '\0');
			total -= 1;
		}
		if (id != 0) {
			do {
				native_fn_0200a8dc(&tmp, tmp.prop.dir.parent);
				tmp.arg.readdir.p_entry = &entry;
				tmp.arg.readdir.skip_string = 0 ;
				MI_WriteByte(dst + total - 1, '/');
				total -= 1;
				while (native_fn_0200a63c(&tmp, FS_COMMAND_READDIR) == FS_RESULT_SUCCESS) {
					if (entry.is_directory && (entry.dir_id.own_id == id)) {
						len = entry.name_len;
						native_fn_02008e0c(entry.name, dst + total - len, len);
						total -= len;
						break;
					}
				}
				id = tmp.prop.dir.pos.own_id;
			} while (id != 0);
		}
		((void) 0) ;
	}
	return FS_RESULT_SUCCESS;
}
