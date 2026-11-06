typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Channel Channel;
typedef void (*ChannelCallback)(Channel *, int, void *);

struct Channel {
    u8 id, type, envelope;
    struct { u8 active:1, start:1, auto_sweep:1, sync:5; } flags;
    u8 pan_range, root;
    s16 user_decay2;
    u8 midi, velocity;
    s8 pan, user_pan;
    s16 user_decay, user_pitch;
    s32 attenuation, sweep_counter, sweep_length;
    u8 attack, sustain;
    u16 decay, release;
    u8 priority, reserved23;
    u16 volume;
    u8 reserved26[2], lfo_parameters[6];
    u16 lfo_delay, lfo_counter;
    s16 sweep_pitch;
    s32 length;
    u8 wave_parameters[12];
    void *wave_data;
    ChannelCallback callback;
    void *callback_data;
    Channel *next;
};

extern u32 native_host_arm7_data_03807eb8[2];
extern const u8 native_host_arm7_data_0380724c[];
extern const u8 native_host_arm7_data_03807250[16];
extern Channel native_host_arm7_data_03807ee0[16];
extern void native_host_arm7_arm_037ffd90(void *);

static inline int compare_volume(Channel *, Channel *);

Channel *native_arm7_wram_037ff950(u32 mask, int priority, u32 flags,
    ChannelCallback callback, void *callback_data)
{
    Channel *selected;
    int index;
    mask &= ~native_host_arm7_data_03807eb8[1];
    if (flags == 0)
        mask &= ~native_host_arm7_data_03807eb8[0];
    selected = 0;
    index = 0;
    do {
        unsigned int id = native_host_arm7_data_03807250[index];
        Channel *current;
        if (!(mask & (1U << id)))
            continue;
        current = &native_host_arm7_data_03807ee0[id];
        if (selected == 0) {
            selected = current;
            continue;
        }
        if (current->priority > selected->priority)
            continue;
        if (current->priority != selected->priority || compare_volume(selected, current) < 0)
            selected = current;
    } while (++index < 16);
    if (selected == 0)
        return 0;
    if (priority < selected->priority)
        return 0;
    if (selected->callback)
        selected->callback(selected, 0, selected->callback_data);
    selected->flags.sync = 2;
    selected->flags.active = 0;
    selected->next = 0;
    selected->callback = callback;
    selected->callback_data = callback_data;
    selected->length = 0;
    selected->priority = priority;
    selected->volume = 127;
    selected->flags.start = 0;
    selected->flags.auto_sweep = 1;
    selected->midi = 60;
    selected->root = 60;
    selected->velocity = 127;
    selected->pan = 0;
    selected->user_decay = 0;
    selected->user_decay2 = 0;
    selected->user_pitch = 0;
    selected->user_pan = 0;
    selected->pan_range = 127;
    selected->sweep_pitch = 0;
    selected->sweep_length = 0;
    selected->sweep_counter = 0;
    selected->attack = 0;
    selected->decay = 65535;
    selected->sustain = 127;
    selected->release = 65535;
    native_host_arm7_arm_037ffd90(selected->lfo_parameters);
    return selected;
}

static inline int compare_volume(Channel *a, Channel *b)
{
    int first = a->volume & 255;
    int second = b->volume & 255;
    first <<= 4;
    second <<= 4;
    first >>= native_host_arm7_data_0380724c[a->volume >> 8];
    second >>= native_host_arm7_data_0380724c[b->volume >> 8];
    if (first != second)
        return first < second ? 1 : -1;
    return 0;
}

