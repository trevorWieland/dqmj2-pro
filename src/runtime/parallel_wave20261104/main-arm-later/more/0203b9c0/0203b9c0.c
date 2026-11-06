#include "context000.h"

void native_main_0203b9c0 (NNSSndStrm * stream, NNSSndStrmCallbackStatus status)
{
    
    const unsigned long blockSize = stream->chBufLen / stream->interval;
    const unsigned long offset = blockSize * stream->curBuffer;
    int index;
    int chNo;
    for (index = 0; index < stream->numChannels; index++) {
        chNo = stream->channelNo[index];
        native_data_020f5b0c[index] = (u8 *)(native_data_020f5b4c[chNo].buffer) + offset;
    }
    stream->callback(
        status,
        stream->numChannels,
        native_data_020f5b0c,
        blockSize,
        stream->format,
        stream->callbackArg
        );
    stream->curBuffer++;
    if (stream->curBuffer >= stream->interval) stream->curBuffer = 0;
}
