typedef unsigned int u32;
typedef struct { u32 words[3]; } Identity;
typedef struct { u32 size; Identity first; Identity second; u32 value; u32 flags; u32 key; u32 reserved[5]; u32 checksum; } Profile;
extern void native_crc32_init(void *, u32);
extern u32 native_crc32_update(const void *, const void *, u32);
extern void native_fill(void *, int, u32);
extern int native_profile_has_value(const Profile *);
extern void native_identity_word1_set(Identity *, u32);
extern int native_identity_kind_set(Identity *, int);
extern int native_identity_kind(const Identity *);
extern u32 native_identity_word1(const Identity *);
extern unsigned long long native_identity_pair(const Identity *);
extern u32 native_identity_code_extract(unsigned long long, u32);
int saved_profile_checksum_valid(const Profile *profile) {
    u32 table[256];
    u32 value;
    native_crc32_init(table, 0xedb88320);
    value = native_crc32_update(table, profile, 60);
    if (value == profile->checksum) return 1;
    return 0;
}
void saved_profile_identity_write(Profile *profile, const Identity *identity, u32 value) {
    u32 table[256];
    profile->second = *identity;
    profile->value = value;
    native_crc32_init(table, 0xedb88320);
    profile->checksum = native_crc32_update(table, profile, 60);
    profile->flags |= 1;
}
int saved_profile_dirty(const Profile *profile) {
    if ((profile->flags & 1) == 1) return 1;
    return 0;
}
void saved_profile_checksum_refresh(Profile *profile) {
    u32 table[256];
    profile->flags &= ~1;
    native_crc32_init(table, 0xedb88320);
    profile->checksum = native_crc32_update(table, profile, 60);
}
void saved_profile_identity_read(const Profile *profile, Identity *identity) {
    native_fill(identity, 0, 12);
    if (native_profile_has_value(profile)) {
        native_identity_word1_set(identity, profile->value);
        native_identity_kind_set(identity, 3);
    } else {
        *identity = profile->first;
    }
}
void saved_identity_word_create(Identity *identity, u32 value) {
    native_fill(identity, 0, 12);
    native_identity_word1_set(identity, value);
    native_identity_kind_set(identity, 3);
}
u32 saved_profile_identity_value(const Profile *profile, const Identity *identity) {
    switch (native_identity_kind(identity)) {
    case 2: return native_identity_code_extract(native_identity_pair(identity), profile->key);
    case 3: return native_identity_word1(identity);
    case 1: return 0xffffffff;
    default: return 0;
    }
}
