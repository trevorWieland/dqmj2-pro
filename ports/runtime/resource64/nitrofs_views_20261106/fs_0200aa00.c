#include "nitrofs_types_20261106.h"
FSResult native_main_0200aa00 (FSFile *p_dir)
{
	FSResult result;
	FSDirEntry *p_entry = p_dir->arg.readdir.p_entry;
	u8 len;
	FSiSyncReadParam param;
	param.arc = p_dir->arc;
	param.pos = p_dir->prop.dir.pos.pos;
	result = native_fn_0200a81c(&param, &len, sizeof(len));
	if (result != FS_RESULT_SUCCESS) {
		return result;
	}
	p_entry->name_len = (u32)(len & ((1 << (7)) - 1) );
	p_entry->is_directory = (u32)((len >> 7) & 1);
	if (p_entry->name_len == 0) {
		result = FS_RESULT_FAILURE;
		return result;
	}
	if (!p_dir->arg.readdir.skip_string) {
		result = native_fn_0200a81c(&param, p_entry->name, p_entry->name_len);
		if (result != FS_RESULT_SUCCESS) {
			return result;
		}
		MI_WriteByte((u8 *)p_entry->name + p_entry->name_len, (u8)'\0');
	} else {
		param.pos += p_entry->name_len;
	}
	if (p_entry->is_directory) {
		u16 id;
		result = native_fn_0200a81c(&param, &id, sizeof(id));
		if (result != FS_RESULT_SUCCESS) {
			return result;
		}
		p_entry->dir_id.arc = p_dir->arc;
		p_entry->dir_id.own_id = (u16)(id & ((1 << (12)) - 1) );
		p_entry->dir_id.index = 0;
		p_entry->dir_id.pos = 0;
	} else {
		p_entry->file_id.arc = p_dir->arc;
		p_entry->file_id.file_id = p_dir->prop.dir.pos.index;
		++p_dir->prop.dir.pos.index;
	}
	p_dir->prop.dir.pos.pos = param.pos;
	return result;
}
