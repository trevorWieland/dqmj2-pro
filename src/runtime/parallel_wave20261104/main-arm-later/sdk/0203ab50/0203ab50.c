#include "context000.h"

#include "context001.h"

void native_main_0203ab50 (LoadCommand * command)
{
    NNSSndStrmPlayer * player = command->player;
    BOOL loopFlag;
    u32 destOffset;
    u32 restSize;
    u32 blockNo;
    u32 blockSize;
    u32 blockSamples;
    u32 blockOffsetSample;
    u32 blockOffset;
    u32 offset;
    u32 samples;
    u32 size;
    u32 readSize;
    int ch;
    if (player->finishFlag && player->finishCounter > 0) {
        player->finishCounter--;
    }
    destOffset = 0;
    restSize = command->bufLen;
    while (restSize > 0) {
        if (player->finishFlag) {
            for (ch = 0; ch < command->numChannels; ch++) {
                MI_CpuClear8((u8 *)(command->buffer[ ch ]) + destOffset, restSize);
            }
            break;
        }
        blockNo = player->curSample / player->info.blockSamples;
        if (blockNo < player->info.numBlocks - 1) {
            blockSize = player->info.blockSize;
            blockSamples = player->info.blockSamples;
        } else {
            blockSize = player->info.lastBlockSize;
            blockSamples = player->info.lastBlockSamples;
        }
        blockOffsetSample = player->curSample;
        blockOffsetSample -= blockNo * player->info.blockSamples;
        samples = restSize;
        if (player->info.format != STRM_FORMAT_PCM8) {
            ((void) 0) ;
            samples >>= 1;
        }
        if (player->dirtyFlag) {
            if (blockOffsetSample == 0) {
                player->dirtyFlag = 0 ;
            } else {
                samples = blockOffsetSample;
                blockOffsetSample = 0;
            }
        }
        loopFlag = 0 ;
        if (blockOffsetSample + samples >= blockSamples) {
            samples = blockSamples - blockOffsetSample;
            if (blockNo >= player->info.numBlocks - 1) {
                if (player->info.loopFlag) {
                    loopFlag = 1 ;
                } else {
                    player->finishFlag = 1 ;
                }
            }
        }
        blockOffset = blockOffsetSample;
        size = samples;
        switch (player->info.format) {
        case STRM_FORMAT_PCM8:
            readSize = size;
            break;
        case STRM_FORMAT_PCM16:
            blockOffset <<= 1;
            size <<= 1;
            readSize = size;
            break;
        case STRM_FORMAT_ADPCM: {
            u32 endSample = blockOffsetSample + samples;
            blockOffset >>= 1;
            endSample++; endSample >>= 1;
            readSize = endSample - blockOffset;
            if (blockOffsetSample == 0) {
                readSize += sizeof(AdpcmState);
            } else {
                blockOffset += sizeof(AdpcmState);
            }
            size <<= 1;
            break;
        }
        }
        offset = blockOffset;
        offset += blockNo * player->info.blockSize * player->info.numChannels;
        offset += player->info.dataOffset;
        for (ch = 0; ch < command->numChannels; ch++) {
            void * dest;
            void * read_dest;
            dest = read_dest = (u8 *)(command->buffer[ ch ]) + destOffset;
            if (ch < player->info.numChannels) {
                s32 resultSize;
                if (player->info.format == STRM_FORMAT_ADPCM) {
                    native_fn_0200708c(&native_data_020f4c9c);
                    read_dest = native_data_020f4c84.decodeBuffer;
                }
                resultSize = player->readStreamFunc(
                    player,
                    read_dest,
                    readSize,
                    offset + ch * blockSize
                    );
                if (resultSize != readSize) {
                    size = 0;
                    samples = 0;
                    loopFlag = 0 ;
                    player->finishFlag = 1 ;
                    if (player->info.format == STRM_FORMAT_ADPCM) {
                        native_fn_02007110(&native_data_020f4c9c);
                    }
                    break;
                }
                if (player->info.format == STRM_FORMAT_ADPCM) {
                    AdpcmState * state = &player->adpcmState[ ch ];
                    u8 * srcp = native_data_020f4c84.decodeBuffer;
                    s16 * destp = dest;
                    u32 i;
                    u32 end;
                    if (blockOffsetSample == 0) {
                        *state = *((AdpcmState *)srcp)++;
                    }
                    end = blockOffsetSample + samples;
                    i = blockOffsetSample;
                    if (i & 0x01) {
                        *destp++ = DecodeAdpcm((*srcp >> 4) & 0x0f, state); i++;
                        srcp++;
                    }
                    while (i < (end & ~0x01)) {
                        *destp++ = DecodeAdpcm(*srcp & 0x0f, state); i++;
                        *destp++ = DecodeAdpcm((*srcp >> 4) & 0x0f, state); i++;
                        srcp++;
                    }
                    if (i < end) {
                        *destp++ = DecodeAdpcm(*srcp & 0x0f, state); i++;
                    }
                    native_fn_02007110(&native_data_020f4c9c);
                }
            } else {
                if (player->monoFlag) {
                    MI_CpuClear8(dest, size);
                } else {
                    native_fn_02008e0c((u8 *)(command->buffer[ 0 ]) + destOffset, dest, size);
                }
            }
        }
        if (player->dirtyFlag) {
            player->dirtyFlag = 0 ;
            continue;
        }
        if (loopFlag) {
            player->curSample = player->info.loopStart;
        } else {
            player->curSample += samples;
        }
        destOffset += size;
        restSize -= size;
        if (player->finishFlag && player->sndArcStrmCallback) {
            native_fn_0203aa0c(player);
        }
    }
    if (player->strmCallback != ((void *)0) ) {
        player->strmCallback(
            command->status,
            command->numChannels,
            command->buffer,
            command->bufLen,
            player->info.format == STRM_FORMAT_PCM8 ? NNS_SND_STRM_FORMAT_PCM8 : NNS_SND_STRM_FORMAT_PCM16,
            player->strmCallbackArg
            );
    }
    for (ch = 0; ch < command->numChannels; ch++) {
        native_fn_02007308(command->buffer[ ch ], command->bufLen);
    }
    if (command->status == NNS_SND_STRM_CALLBACK_SETUP) {
        player->prepareFlag = 1 ;
    }
}
