typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef struct NativePlayerFlags { u8 active : 1; u8 prepared : 1; u8 paused : 1; u8 reserved : 5; } NativePlayerFlags;
typedef struct NativePlayerView {
    NativePlayerFlags flags;
    u8 playerId;
    u8 reserved02[3];
    u8 volume;
    s16 fader;
    u8 tracks[16];
    u16 tempo;
    u16 ratio;
    u16 accumulator;
    u16 reserved1E;
    void *bank;
} NativePlayerView;
typedef struct NativeSharedCounter { s16 values[16]; u32 counter; } NativeSharedCounter;
typedef struct NativeSharedView { u32 reserved00; u32 status; u8 reserved08[24]; NativeSharedCounter counters[16]; } NativeSharedView;
typedef struct NativeSharedCounterCursor { u8 reserved[64]; u32 counter; } NativeSharedCounterCursor;
typedef char PlayerSize[(sizeof(NativePlayerView) == 36) ? 1 : -1];
extern NativePlayerView native_host_arm7_data_03808420[];
extern NativeSharedView *native_host_arm7_data_03807edc;
extern int native_host_arm7_arm_03800cf0(NativePlayerView *, int);
extern void native_host_arm7_arm_03800b00(NativePlayerView *);
extern void *native_host_arm7_arm_03800a7c(NativePlayerView *, int);
extern void native_host_arm7_arm_03800b98(void *, NativePlayerView *, int);
void native_arm7_wram_037fff54(int step) {
    NativePlayerView *player;
    void *track;
    int index;
    u32 status = 0;
    int tick;
    int ticks;
    int slot;
    int increment;
    index = 0;
    do {
        player = &native_host_arm7_data_03808420[index];
        if (player->flags.active) {
            if (player->flags.prepared) {
                if (step && !player->flags.paused) {
                    ticks = 0;
                    while (player->accumulator >= 240) {
                        player->accumulator -= 240;
                        ticks++;
                    }
                    for (tick = 0; tick < ticks; tick++) {
                        if (native_host_arm7_arm_03800cf0(player, 1)) {
                            native_host_arm7_arm_03800b00(player);
                            break;
                        }
                    }
                    if (native_host_arm7_data_03807edc)
                        ((NativeSharedCounterCursor *)((u8 *)native_host_arm7_data_03807edc + player->playerId * 36))->counter += tick;
                    increment = player->tempo;
                    increment = (int)((u32)increment * player->ratio);
                    increment >>= 8;
                    player->accumulator += increment;
                }
                slot = 0;
                do {
                    track = native_host_arm7_arm_03800a7c(player, slot);
                    if (track)
                        native_host_arm7_arm_03800b98(track, player, 1);
                    slot++;
                } while (slot < 16);
            }
            if (player->flags.active)
                status |= 1u << index;
        }
        index++;
    } while (index < 16);
    if (native_host_arm7_data_03807edc)
        native_host_arm7_data_03807edc->status = status;
}
