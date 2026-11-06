#include "context_00.h"
BOOL native_main_0203988c (SNDWaveArc * waveArc, int waveNo, u32 fileId, NNSSndHeapHandle heap)
{
    SNDWaveData * buffer;
    u32 len;
    u32 begin;
    u32 end;
    u32 waveCount;
    ((void) 0) ;
    if (native_fn_0200a288(waveArc, waveNo) != ((void *)0) ) {
        return 1 ;
    }
    waveCount = native_fn_0200a24c(waveArc);
    begin = waveArc->waveOffset[ waveArc->waveCount + waveNo ];
    if (waveNo < waveCount - 1) {
        end = waveArc->waveOffset[ waveArc->waveCount + waveNo + 1 ];
    } else {
        end = waveArc->fileHeader.fileSize;
    }
    len = end - begin;
    if (heap == ((void *)0) ) {
        return 0 ;
    }
    buffer = (SNDWaveData *)native_fn_02037b94(
        heap,
        len + 32 ,
        native_fn_02039844,
        (u32)waveArc,
        (u32)waveNo
        );
    if (buffer == ((void *)0) ) return 0 ;
    if (native_fn_02039094(fileId, buffer, (s32)len, (s32)begin) != len) {
        return 0 ;
    }
    native_fn_020072ec(buffer, len);
    native_fn_0200a254(waveArc, waveNo, buffer);
    return 1 ;
}
