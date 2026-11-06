#include "context000.h"

void native_main_0203b560 (NNSSndStrm * stream)
{
    ((void) 0) ;
    {
        
        if (!native_data_020f5afc) {
            native_fn_0202b9dc(&native_data_020f5b00, ((unsigned int)&((( NNSSndStrm*)0)-> link))) ;
            native_data_020f5afc = 1 ;
        }
    }
    PM_SetSleepCallbackInfo(&stream->preSleepInfo, native_fn_0203ba70, stream);
    PM_SetSleepCallbackInfo(&stream->postSleepInfo, native_fn_0203babc, stream);
    stream->chBitMask = 0;
    stream->numChannels = 0;
    stream->activeFlag = 0 ;
    stream->startFlag = 0 ;
}

#include "context001.h"
