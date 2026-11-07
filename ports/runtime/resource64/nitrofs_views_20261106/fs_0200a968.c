#include "nitrofs_types_20261106.h"
FSResult native_main_0200a968 (FSFile *p_dir)
{
	FSResult result;
	FSArchive *const p_arc = p_dir->arc;
	const FSDirPos *const arg = &p_dir->arg.seekdir.pos;
	FSArchiveFNT fnt_entry;
	FSiSyncReadParam param;
	param.arc = p_arc;
	param.pos = p_arc->fnt + arg->own_id * sizeof(fnt_entry);
	result = native_fn_0200a81c(&param, &fnt_entry, sizeof(fnt_entry));
	if (result == FS_RESULT_SUCCESS) {
		p_dir->prop.dir.pos = *arg;
		if ((arg->index == 0) && (arg->pos == 0)) {
			p_dir->prop.dir.pos.index = fnt_entry.index;
			p_dir->prop.dir.pos.pos = p_arc->fnt + fnt_entry.start;
		}
		p_dir->prop.dir.parent = (u32)(fnt_entry.parent & ((1 << (12)) - 1) );
	}
	return result;
}
