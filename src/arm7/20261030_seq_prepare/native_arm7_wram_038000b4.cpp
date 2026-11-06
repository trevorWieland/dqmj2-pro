extern "C" {
typedef unsigned char u8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;

typedef struct PlayerFlags {
    u8 active:1, prepared:1, paused:1, reserved:5;
} PlayerFlags;

typedef struct Player {
    PlayerFlags flags;
    u8 id, reserved02[2], priority, volume;
    s16 fader;
    u8 tracks[16];
    u16 tempo, ratio, counter;
    u8 reserved1E[2];
    const void *bank;
} Player;

typedef struct Track {
    u8 reserved00[0x24];
    const u8 *base, *current;
    u8 reserved2C[0x14];
} Track;

typedef struct SharedPlayer {
    s16 variables[16];
    u32 counter;
} SharedPlayer;

typedef struct Shared {
    u32 reserved00, player_status;
    u8 reserved08[24];
    SharedPlayer players[16];
} Shared;

typedef char PlayerSize[(sizeof(Player) == 36) ? 1 : -1];
typedef char TrackSize[(sizeof(Track) == 64) ? 1 : -1];
typedef struct Work {
    u8 channels[0x540];
    Player players[16];
    Track tracks[32];
} Work;
extern Work native_host_arm7_data_03807ee0;
extern Shared *native_host_arm7_data_03807edc;
extern void native_host_arm7_arm_03800b00(Player *);
extern int native_host_arm7_arm_03801884(void);
extern void native_host_arm7_arm_038008f0(Track *);
extern void native_host_arm7_arm_03800784(const u8 *);
extern u8 native_host_arm7_arm_03800290(Track *);

static inline void initialize_player(Player *, const void *);
static inline void start_track(Track *, const u8 *, u32);
static inline u16 read_halfword(Track *);

void native_arm7_wram_038000b4(int player_index, const u8 *sequence, u32 offset, const void *bank)
{
    Player *player = &native_host_arm7_data_03807ee0.players[player_index];
    if (player->flags.active)
        native_host_arm7_arm_03800b00(player);
    initialize_player(player, bank);
    int allocated = native_host_arm7_arm_03801884();
    if (allocated < 0)
        return;
    Track *track = &native_host_arm7_data_03807ee0.tracks[allocated];
    native_host_arm7_arm_038008f0(track);
    start_track(track, sequence, offset);
    player->tracks[0] = allocated;
    native_host_arm7_arm_03800784(track->current);
    u8 command = native_host_arm7_arm_03800290(track);
    if (command != 254) {
        track->current--;
    } else {
        int index;
        u16 mask;
        for (mask = read_halfword(track) >> 1, index = 1; mask != 0; index++, mask >>= 1) {
            if (mask & 1) {
                allocated = native_host_arm7_arm_03801884();
                if (allocated < 0)
                    break;
                native_host_arm7_arm_038008f0(&native_host_arm7_data_03807ee0.tracks[allocated]);
                player->tracks[index] = allocated;
            }
        }
    }
    player->flags.active = 1;
    player->flags.prepared = 0;
    if (native_host_arm7_data_03807edc)
        native_host_arm7_data_03807edc->player_status |= 1U << player_index;
}

static inline void initialize_player(Player *player, const void *bank)
{
    int index;
    player->flags.paused = 0;
    player->bank = bank;
    player->tempo = 120;
    player->ratio = 256;
    player->counter = 240;
    player->volume = 127;
    player->fader = 0;
    player->priority = 64;
    index = 0;
    do {
        player->tracks[index] = 255;
    } while (++index < 16);
    if (native_host_arm7_data_03807edc) {
        native_host_arm7_data_03807edc->players[player->id].counter = 0;
        int variable = 0;
        do {
            native_host_arm7_data_03807edc->players[player->id].variables[variable] = -1;
        } while (++variable < 16);
    }
}

static inline void start_track(Track *track, const u8 *sequence, u32 offset)
{
    track->base = sequence;
    track->current = sequence + offset;
}

static inline u16 read_halfword(Track *track)
{
    u32 low = native_host_arm7_arm_03800290(track);
    u32 high = native_host_arm7_arm_03800290(track);
    return low | high << 8;
}

}
