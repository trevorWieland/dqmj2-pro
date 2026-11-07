#include "context000.h"

#include "context001.h"

void native_host_arm7_wram_03801f1c (void)
{
    OSMessage message;
    const SNDCommand * command_p;
    SNDCommand command;
    while (native_host_arm7_arm_037fc760(&native_host_arm7_data_03809060, &message, 0 )) {
        command_p = (const SNDCommand *)message;
        while (command_p != ((void *)0) ) {
            command = *command_p;
            switch (command.id) {
            case SND_COMMAND_START_SEQ:
                native_host_arm7_arm_03800310((int)command.arg[0],
                             (const void *)command.arg[1],
                             command.arg[2], (struct SNDBankData *)command.arg[3]);
                break;
            case SND_COMMAND_STOP_SEQ:
                native_host_arm7_arm_03800340((int)command.arg[0]);
                break;
            case SND_COMMAND_PREPARE_SEQ:
                native_host_arm7_arm_038000b4((int)command.arg[0],
                               (const void *)command.arg[1],
                               command.arg[2], (struct SNDBankData *)command.arg[3]);
                break;
            case SND_COMMAND_START_PREPARED_SEQ:
                native_host_arm7_arm_038002f0((int)command.arg[0]);
                break;
            case SND_COMMAND_PAUSE_SEQ:
                native_host_arm7_arm_0380039c((int)command.arg[0], (BOOL)command.arg[1]);
                break;
            case SND_COMMAND_SKIP_SEQ:
                native_host_arm7_arm_03800414((int)command.arg[0], (u32)command.arg[1]);
                break;
            case SND_COMMAND_PLAYER_PARAM:
                native_host_arm7_arm_038006a4((int)command.arg[0],
                                    command.arg[1], command.arg[2], (int)command.arg[3]);
                break;
            case SND_COMMAND_TRACK_PARAM:
                native_host_arm7_arm_038006e8((int)(((command.arg[0]) >> ( 0)) & ((1 << ( 24)) - 1)) ,
                                   command.arg[1],
                                   command.arg[2],
                                   command.arg[3], (int)(((command.arg[0]) >> ( 24)) & ((1 << ( 8)) - 1)) );
                break;
            case SND_COMMAND_MUTE_TRACK:
                native_host_arm7_arm_038004e0((int)command.arg[0], command.arg[1], (SNDSeqMute) command.arg[2]);
                break;
            case SND_COMMAND_ALLOCATABLE_CHANNEL:
                native_host_arm7_arm_0380054c((int)command.arg[0], command.arg[1], command.arg[2]);
                break;
            case SND_COMMAND_PLAYER_LOCAL_VAR:
                native_host_arm7_arm_03801c50((int)command.arg[0],
                                           (int)command.arg[1], (s16)command.arg[2]);
                break;
            case SND_COMMAND_PLAYER_GLOBAL_VAR:
                native_host_arm7_arm_03801c70((int)command.arg[0], (s16)command.arg[1]);
                break;
            case SND_COMMAND_START_TIMER:
                StartTimer(command.arg[0], command.arg[1], command.arg[2], command.arg[3]);
                break;
            case SND_COMMAND_STOP_TIMER:
                StopTimer(command.arg[0], command.arg[1], command.arg[2], command.arg[3]);
                break;
            case SND_COMMAND_SETUP_CAPTURE:
                native_host_arm7_arm_037ff0fc((SNDCapture)(((command.arg[2]) >> ( 31)) & ((1 << ( 1)) - 1)) ,
                                 (SNDCaptureFormat)(((command.arg[2]) >> ( 30)) & ((1 << ( 1)) - 1)) ,
                                 (void *)command.arg[0],
                                 (int)command.arg[1],
                                 (BOOL)(((command.arg[2]) >> ( 29)) & ((1 << ( 1)) - 1)) ,
                                 (SNDCaptureIn)(((command.arg[2]) >> ( 28)) & ((1 << ( 1)) - 1)) ,
                                 (SNDCaptureOut)(((command.arg[2]) >> ( 27)) & ((1 << ( 1)) - 1)) );
                break;
            case SND_COMMAND_SETUP_ALARM:
                native_host_arm7_arm_03801d50((int)command.arg[0],
                               (OSTick)command.arg[1], (OSTick)command.arg[2], (int)command.arg[3]);
                break;
            case SND_COMMAND_CHANNEL_TIMER:
                SetChannelTimer((u32)command.arg[0], (int)command.arg[1]);
                break;
            case SND_COMMAND_CHANNEL_VOLUME:
                SetChannelVolume((u32)command.arg[0],
                                 (int)command.arg[1], (SNDChannelDataShift)command.arg[2]);
                break;
            case SND_COMMAND_CHANNEL_PAN:
                SetChannelPan((u32)command.arg[0], (int)command.arg[1]);
                break;
            case SND_COMMAND_SETUP_CHANNEL_PCM:
                native_host_arm7_arm_037fe804((int)(((command.arg[0]) >> ( 0)) & ((1 << ( 16)) - 1)) ,
                                    (const void *)(((command.arg[1]) >> ( 0)) & ((1 << ( 27)) - 1)) ,
                                    (SNDWaveFormat)(((command.arg[3]) >> ( 24)) & ((1 << ( 2)) - 1)) ,
                                    (SNDChannelLoop)(((command.arg[3]) >> ( 26)) & ((1 << ( 2)) - 1)) ,
                                    (int)(((command.arg[3]) >> ( 0)) & ((1 << ( 16)) - 1)) ,
                                    (int)(((command.arg[2]) >> ( 0)) & ((1 << ( 22)) - 1)) ,
                                    (int)(((command.arg[2]) >> ( 24)) & ((1 << ( 7)) - 1)) ,
                                    (SNDChannelDataShift)(((command.arg[2]) >> ( 22)) & ((1 << ( 2)) - 1)) ,
                                    (int)(((command.arg[0]) >> ( 16)) & ((1 << ( 16)) - 1)) ,
                                    (int)(((command.arg[3]) >> ( 16)) & ((1 << ( 7)) - 1))
                                    );
                break;
            case SND_COMMAND_SETUP_CHANNEL_PSG:
                native_host_arm7_arm_037fe8d0((int)command.arg[0],
                                    (SNDDuty)command.arg[3],
                                    (int)(((command.arg[1]) >> ( 0)) & ((1 << ( 7)) - 1)) ,
                                    (SNDChannelDataShift)(((command.arg[1]) >> ( 8)) & ((1 << ( 2)) - 1)) ,
                                    (int)(((command.arg[2]) >> ( 8)) & ((1 << ( 16)) - 1)) ,
                                    (int)(((command.arg[2]) >> ( 0)) & ((1 << ( 7)) - 1))
                                    );
                break;
            case SND_COMMAND_SETUP_CHANNEL_NOISE:
                native_host_arm7_arm_037fe97c((int)command.arg[0],
                                      (int)(((command.arg[1]) >> ( 0)) & ((1 << ( 7)) - 1)) ,
                                      (SNDChannelDataShift)(((command.arg[1]) >> ( 8)) & ((1 << ( 2)) - 1)) ,
                                      (int)(((command.arg[2]) >> ( 8)) & ((1 << ( 16)) - 1)) ,
                                      (int)(((command.arg[2]) >> ( 0)) & ((1 << ( 7)) - 1))
                                      );
                break;
            case SND_COMMAND_SURROUND_DECAY:
                native_host_arm7_arm_037febe0((int)command.arg[0]);
                break;
            case SND_COMMAND_MASTER_VOLUME:
                native_host_arm7_arm_037fe7bc((int)command.arg[0]);
                break;
            case SND_COMMAND_MASTER_PAN:
                native_host_arm7_arm_037feb6c((int)command.arg[0]);
                break;
            case SND_COMMAND_OUTPUT_SELECTOR:
                native_host_arm7_arm_037fe7cc((SNDOutput)command.arg[0],
                                      (SNDOutput)command.arg[1],
                                      (SNDChannelOut)command.arg[2], (SNDChannelOut)command.arg[3]);
                break;
            case SND_COMMAND_LOCK_CHANNEL:
                native_host_arm7_arm_037ffbe0(command.arg[0], command.arg[1]);
                break;
            case SND_COMMAND_UNLOCK_CHANNEL:
                native_host_arm7_arm_037ffcc0(command.arg[0], command.arg[1]);
                break;
            case SND_COMMAND_STOP_UNLOCKED_CHANNEL:
                native_host_arm7_arm_037ffb30(command.arg[0], command.arg[1]);
                break;
            case SND_COMMAND_INVALIDATE_SEQ:
                native_host_arm7_arm_038005bc((const void *)command.arg[0], (const void *)command.arg[1]);
                break;
            case SND_COMMAND_INVALIDATE_BANK:
                native_host_arm7_arm_03800648((const void *)command.arg[0], (const void *)command.arg[1]);
                break;
            case SND_COMMAND_INVALIDATE_WAVE:
                native_host_arm7_arm_037ffd14((const void *)command.arg[0], (const void *)command.arg[1]);
                break;
            case SND_COMMAND_SHARED_WORK:
                native_host_arm7_data_03807edc = (SNDSharedWork *)command.arg[0];
                break;
            case SND_COMMAND_READ_DRIVER_INFO:
                ReadDriverInfo((SNDDriverInfo *) command.arg[0]);
                break;
            }
            command_p = command.next;
        }
        ((void) 0) ;
        native_host_arm7_data_03807edc->finishCommandTag++;
    }
}

#include "context002.h"
