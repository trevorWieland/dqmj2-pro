#include "context000.h"

void native_main_0203b870 (NNSSndStrm * stream, int volume)
{
    u16 chVolume;
    int vol;
    int chNo;
    int i;
    ((void) 0) ;
    stream->volume = volume;
    for (i = 0; i < stream->numChannels; i++) {
        chNo = stream->channelNo[ i ];
        vol = stream->volume + native_data_020f5b4c[ chNo ].volume;
        chVolume = native_fn_02009e60(vol);
        native_fn_020092e4(
            (u32)(1 << chNo),
            chVolume & 0xff,
            (SNDChannelDataShift)(chVolume >> 8)
            );
    }
}
