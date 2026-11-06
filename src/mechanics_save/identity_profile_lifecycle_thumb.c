#pragma opt_strength_reduction on
typedef unsigned int u32;
typedef unsigned long long u64;
typedef struct { u32 words[3]; } Identity;
typedef struct { u32 size; Identity first; Identity second; u32 value; u32 flags; u32 key; u32 reserved[5]; u32 checksum; } Profile;
extern void native_seed_words(u32 *);
typedef struct { u64 primary; u64 secondary; u32 present; } Context;
extern void native_context_words(void *);
void saved_sdk_context_snapshot(Context *);
extern void native_identity_login_set(Identity *, u32, u32);
extern void native_identity_word2_set(Identity *, u32);
extern int native_identity_kind_set(Identity *, int);
extern int native_identity_kind(const Identity *);
extern u64 native_identity_login(const Identity *);
extern void native_fill(void *, int, u32);
extern void native_crc32_init(void *, u32);
extern u32 native_crc32_update(const void *, const void *, u32);
void saved_identity_seed_initialize(Identity *identity) {
    Context context;
    u32 words[8];
    u64 seed;
    u32 index;
    native_seed_words(words);
    index = 1;
    do { words[index] ^= words[index - 1]; index++; } while (index < 8);
    seed = words[7];
    saved_sdk_context_snapshot(&context);
    if (context.present) native_identity_login_set(identity, (u32)context.primary, (u32)(context.primary >> 32));
    else native_identity_login_set(identity, (u32)context.secondary, (u32)(context.secondary >> 32));
    native_identity_word2_set(identity, (u32)((((u64)seed * 0x5d588b656c078965ULL) + 1ULL) >> 32));
    native_identity_kind_set(identity, 1);
}
void saved_profile_initialize(Profile *profile, u32 key) {
    u32 table[256];
    native_fill(profile, 0, 64);
    profile->size = 64;
    profile->value = 0;
    profile->key = key;
    saved_identity_seed_initialize(&profile->first);
    native_identity_kind_set(&profile->second, 0);
    native_crc32_init(table, 0xedb88320);
    profile->checksum = native_crc32_update(table, profile, 60);
    profile->flags |= 1;
}
int saved_identity_context_equal(const Identity *identity) {
    Context context;
    saved_sdk_context_snapshot(&context);
    if (context.present) {
        if (native_identity_login(identity) == context.primary) return 1;
        return 0;
    }
    if (native_identity_login(identity) == context.secondary) return 1;
    return 0;
}
int saved_profile_context_equal(const Profile *profile) {
    Context context;
    if (native_identity_kind(&profile->second) == 0) return 1;
    saved_sdk_context_snapshot(&context);
    if (context.present == 0) return 0;
    if (native_identity_login(&profile->second) == context.primary) return 1;
    return 0;
}
void saved_sdk_context_snapshot(Context *output) {
    Context context;
    native_context_words(&context);
    output->primary = context.primary;
    output->secondary = context.secondary;
    if (context.primary == 0) output->present = 0;
    else output->present = 1;
}
