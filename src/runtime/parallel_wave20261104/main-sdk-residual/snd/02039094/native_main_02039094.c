#include "context_00.h"
s32 native_main_02039094 (u32 fileId, void * buffer, s32 size, s32 offset)
{
    NNSSndArc * arc = native_data_main_020f4c44.field_0000;
    const NNSSndArcFileInfo * file;
    s32 totalReadSize;
    s32 readSize;
    s32 blockSize;
    s32 currentOffset;
    s32 requestSize;
    u8 * destAddress;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    ((void) 0) ;
    if (fileId >= arc->fat->count) return -1;
    file = &arc->fat->files[ fileId ];
    currentOffset = offset;
    blockSize = arc->loadBlockSize;
    if (blockSize == 0) {
        blockSize = size;
    }
    totalReadSize = 0;
    destAddress = (u8 *)buffer;
    while (totalReadSize < size) {
        requestSize = size - totalReadSize;
        if (requestSize > blockSize) requestSize = blockSize;
        if (requestSize > file->size - currentOffset) {
            requestSize = (s32)(file->size - currentOffset);
        }
        if (requestSize == 0) {
            break;
        }
        if (!native_fn_0200c190(&arc->file, (s32)(file->offset + currentOffset), FS_SEEK_SET)) {
            return -1;
        }
        readSize = native_fn_0200c180(&arc->file, destAddress, requestSize);
        if (readSize < 0) return readSize;
        totalReadSize += readSize;
        currentOffset += readSize;
        destAddress += readSize;
    }
    return totalReadSize;
}
