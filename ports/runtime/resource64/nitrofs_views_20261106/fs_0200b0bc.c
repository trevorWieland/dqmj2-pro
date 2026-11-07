#include "nitrofs_types_20261106.h"
FSResult native_main_0200b0bc (FSFile *p_file)
{
	FSResult result;
	FSArchive *const p_arc = p_file->arc;
	const FSFileID *p_id = &p_file->arg.openfilefast.id;
	const u32 index = p_id->file_id;
	{
		u32 pos = (u32)(index * sizeof(FSArchiveFAT));
        if (pos >= p_arc->fat_size) {
			result = FS_RESULT_FAILURE;
		} else {
			FSArchiveFAT fat;
			FSiSyncReadParam param;
            param.arc = p_arc;
			param.pos = p_arc->fat + pos;
			result = native_fn_0200a81c(&param, &fat, sizeof(fat));
			if (result == FS_RESULT_SUCCESS) {
				p_file->arg.openfiledirect.top = fat.top;
				p_file->arg.openfiledirect.bottom = fat.bottom;
				p_file->arg.openfiledirect.index = index;
				result = native_fn_0200a63c(p_file, FS_COMMAND_OPENFILEDIRECT);
			}
		}
	}
	return result;
}
