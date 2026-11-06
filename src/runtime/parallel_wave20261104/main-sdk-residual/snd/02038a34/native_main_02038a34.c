#include "context_00.h"
BOOL native_main_02038a34 (NNSSndArc * arc, const char * filePath, NNSSndHeapHandle heap, BOOL symbolLoadFlag)
{
    BOOL result;
    ((void) 0) ;
    ((void) 0) ;
    arc->info = ((void *)0) ;
    arc->fat = ((void *)0) ;
    arc->symbol = ((void *)0) ;
    arc->loadBlockSize = 0;
    result = native_fn_0200beec(&arc->fileId, filePath);
    if (!result) return 0 ;
    native_fn_0200bd04(&arc->file);
    result = native_fn_0200bf74(&arc->file, arc->fileId);
    if (!result) return 0 ;
    arc->file_open = 1 ;
    result = native_fn_02038ac4(arc, heap, symbolLoadFlag);
    if (!result) return 0 ;
    native_data_main_020f4c44.field_0000 = arc;
    return 1 ;
}
