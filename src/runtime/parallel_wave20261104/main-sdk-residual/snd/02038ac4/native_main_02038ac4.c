#include "context_00.h"
BOOL native_main_02038ac4 (NNSSndArc * arc, NNSSndHeapHandle heap, BOOL symbolLoadFlag)
{
    BOOL result;
    s32 readSize;
    ((void) 0) ;
    ((void) 0) ;
    result = native_fn_0200c190(&arc->file, 0, FS_SEEK_SET);
    if (!result) return 0 ;
    readSize = native_fn_0200c180(
        &arc->file,
        &arc->header,
        sizeof(arc->header)
        );
    if (readSize != sizeof(arc->header)) return 0 ;
    ((void) 0)
        ;
    ((void) 0) ;
    if (heap != ((void *)0) ) {
        arc->info = (NNSSndArcInfo *)native_fn_02037b94(heap, arc->header.infoSize, native_fn_020391c0, (u32)arc, 0);
        if (arc->info == ((void *)0) ) return 0 ;
        result = native_fn_0200c190(&arc->file, (s32)(arc->header.infoOffset), FS_SEEK_SET);
        if (!result) return 0 ;
        readSize = native_fn_0200c180(&arc->file, arc->info, (s32)(arc->header.infoSize));
        if (readSize != arc->header.infoSize) return 0 ;
        ((void) 0) ;
        arc->fat = (NNSSndArcFat *)native_fn_02037b94(heap, arc->header.fatSize, native_fn_020391cc, (u32)arc, 0);
        if (arc->fat == ((void *)0) ) return 0 ;
        result = native_fn_0200c190(&arc->file, (s32)(arc->header.fatOffset), FS_SEEK_SET);
        if (!result) return 0 ;
        readSize = native_fn_0200c180(&arc->file, arc->fat, (s32)(arc->header.fatSize));
        if (readSize != arc->header.fatSize) return 0 ;
        ((void) 0) ;
        if (symbolLoadFlag && arc->header.symbolDataSize > 0) {
            arc->symbol = (NNSSndArcSymbol *)native_fn_02037b94(heap, arc->header.symbolDataSize, native_fn_020391d8, (u32)arc, 0);
            if (arc->symbol == ((void *)0) ) return 0 ;
            result = native_fn_0200c190(&arc->file, (s32)(arc->header.symbolDataOffset), FS_SEEK_SET);
            if (!result) return 0 ;
            readSize = native_fn_0200c180(&arc->file, arc->symbol, (s32)(arc->header.symbolDataSize));
            if (readSize != arc->header.symbolDataSize) return 0 ;
            ((void) 0) ;
        }
    }
    return 1 ;
}
