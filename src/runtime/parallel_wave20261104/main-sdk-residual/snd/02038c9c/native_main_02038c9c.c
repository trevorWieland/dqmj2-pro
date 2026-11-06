#include "context_00.h"
void native_main_02038c9c (NNSSndArc * arc, void * data)
{
    NNSSndArcHeader * header = (NNSSndArcHeader *)data;
    NNSSndArcFileInfo * file;
    int fileId;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    MI_CpuCopy32(header, &arc->header, sizeof(arc->header));
    ((void) 0)        ;
    ((void) 0) ;
    arc->info = (NNSSndArcInfo *)GetPtr(header, arc->header.infoOffset);
    arc->fat = (NNSSndArcFat *)GetPtr(header, arc->header.fatOffset);
    arc->symbol = (NNSSndArcSymbol *)GetPtr(header, arc->header.symbolDataOffset);
    arc->loadBlockSize = 0;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    for (fileId = 0; fileId < arc->fat->count; fileId++) {
        file = &arc->fat->files[ fileId ];
        file->mem = GetPtr(header, file->offset);
        ((void) 0) ;
    }
    arc->file_open = 0 ;
    native_data_main_020f4c44.field_0000 = arc;
}
