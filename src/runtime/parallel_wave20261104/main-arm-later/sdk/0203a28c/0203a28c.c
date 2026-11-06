#include "context000.h"

BOOL native_main_0203a28c (struct NNSSndStrmHandle * handle, const NNSSndArcStrmInfo * strmInfo, int playerNo, int playerPrio, int strmNo, u32 offset, NNSSndStrmCallback strmCallback, void * strmCallbackArg, NNSSndArcStrmCallback sndArcStrmCallback, void * sndArcStrmCallbackArg)
{
    NNSSndStrmPlayer * player;
    NNSSndStrmFormat format;
    int numChannels;
    u64 tmpU64;
    BOOL ret;
    ((void) 0) ;
    ((void) 0) ;
    player = native_fn_0203a1d4(handle, playerNo, playerPrio);
    if (player == ((void *)0) ) return 0 ;
    native_fn_0203b378(player, strmInfo->fileId);
    if (!player->openStreamFunc(player, strmInfo->fileId)) {
        native_fn_0203a260(player);
        return 0 ;
    }
    tmpU64 = player->info.sampleRate;
    tmpU64 *= offset;
    tmpU64 /= 1000;
    player->curSample = (u32)tmpU64;
    if (player->curSample != 0 && player->info.format == STRM_FORMAT_ADPCM) {
        player->dirtyFlag = 1 ;
    } else {
        player->dirtyFlag = 0 ;
    }
    player->finishCounter = 4 ;
    player->finishFlag = 0 ;
    player->playFlag = 0 ;
    player->prepareFlag = 0 ;
    player->startFlag = 0 ;
    player->fadeOutFlag = 0 ;
    player->commandCount = 0;
    player->strmCallback = strmCallback;
    player->strmCallbackArg = strmCallbackArg;
    player->sndArcStrmCallback = sndArcStrmCallback;
    player->sndArcStrmCallbackArg = sndArcStrmCallbackArg;
    player->strmNo = strmNo;
    player->volume = 0;
    player->initVolume = strmInfo->volume;
    player->extVolume = 127;
    native_fn_020379ac(&player->fader);
    native_fn_020379c4(&player->fader, 127 << 8, 1);
    switch (player->info.format) {
    case STRM_FORMAT_PCM8:
        format = NNS_SND_STRM_FORMAT_PCM8;
        break;
    case STRM_FORMAT_PCM16:
    case STRM_FORMAT_ADPCM:
        format = NNS_SND_STRM_FORMAT_PCM16;
        break;
    }
    numChannels = player->info.numChannels;
    if (strmInfo->flags & (1 << 0) ) {
        numChannels = 2;
    }
    if (numChannels > player->numChannels) {
        numChannels = player->numChannels;
    }
    player->monoFlag = (numChannels == 1) ? 1 : 0 ;
    ret = native_fn_0203a650(player, numChannels, player->chNoList);
    if (!ret) {
        player->closeStreamFunc(player);
        native_fn_0203a260(player);
        return 0 ;
    }
    ret = native_fn_0203b660(
        &player->stream,
        format,
        player->buffer,
        player->bufSize * numChannels / player->numChannels,
        player->info.timer,
        4 ,
        native_fn_0203a8d4,
        player
        );
    if (!ret) {
        native_fn_0203a688(player);
        player->closeStreamFunc(player);
        native_fn_0203a260(player);
        return 0 ;
    }
    if (numChannels == 2) {
        native_fn_0203b8dc(&player->stream, 0, 0);
        native_fn_0203b8dc(&player->stream, 1, 127);
    }
    return 1 ;
}

#include "context001.h"
