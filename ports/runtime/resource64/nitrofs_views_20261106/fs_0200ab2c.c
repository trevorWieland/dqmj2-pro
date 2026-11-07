#include "nitrofs_types_20261106.h"
FSResult native_main_0200ab2c (FSFile *p_dir)
{
	const char *path = p_dir->arg.findpath.path;
	const BOOL is_dir = p_dir->arg.findpath.find_directory;
	p_dir->arg.seekdir.pos = p_dir->arg.findpath.pos;
	(void)native_fn_0200a63c(p_dir, FS_COMMAND_SEEKDIR);
	for (; MI_ReadByte(path); path += (MI_ReadByte(path) ? 1 : 0)) {
		u32 is_directory;
		int name_len = 0;
		while ((is_directory = MI_ReadByte(path + name_len)),
		       (is_directory && !FSi_IsSlash(is_directory)))
			++name_len;
		if (is_directory || is_dir)
			is_directory = 1;
		if (name_len == 0) {
			return FS_RESULT_FAILURE;
		} else if (MI_ReadByte(path) == '.')   {
			if (name_len == 1) {
				path += 1;
				continue;
			} else if ((name_len == 2) & (MI_ReadByte(path + 1) == '.'))   {
				if (p_dir->prop.dir.pos.own_id != 0)
					native_fn_0200a8dc(p_dir, p_dir->prop.dir.parent);
				path += 2;
				continue;
			}
		}
		if (name_len > 127 ) {
			return FS_RESULT_FAILURE;
		} else {
			FSDirEntry etr;
			p_dir->arg.readdir.p_entry = &etr;
			p_dir->arg.readdir.skip_string = 0 ;
			for (;;) {
				if (native_fn_0200a63c(p_dir, FS_COMMAND_READDIR) != FS_RESULT_SUCCESS)
					return FS_RESULT_FAILURE;
				if ((is_directory != etr.is_directory) ||
				    (name_len != etr.name_len) || native_fn_0200a7cc(path, etr.name, (u32)name_len))
					continue;
				if (is_directory) {
					path += name_len;
					p_dir->arg.seekdir.pos = etr.dir_id;
					(void)native_fn_0200a63c(p_dir, FS_COMMAND_SEEKDIR);
					break;
				} else if (is_dir)   {
					return FS_RESULT_FAILURE;
				} else {
					*p_dir->arg.findpath.result.file = etr.file_id;
					return FS_RESULT_SUCCESS;
				}
			}
		}
	}
	if (!is_dir)
		return FS_RESULT_FAILURE;
	*p_dir->arg.findpath.result.dir = p_dir->prop.dir.pos;
	return FS_RESULT_SUCCESS;
}
