typedef unsigned char u8;
typedef unsigned int u32;
typedef unsigned long long u64;
extern void native_crc_init(void *, int);
extern u32 native_crc_update(const void *, const void *, u32);
extern void native_md5_init(void *);
extern void native_md5_update(void *, const void *, u32);
extern void native_md5_finish(void *, void *);
extern int native_sdk_flags(const void *);
extern int native_sdk_flags_set(void *, u32);
extern void native_sdk_pair_set(void *, u32, u32);
extern void native_fill(void *, int, u32);
u64 saved_identity_code(u32 identity, u32 key, int mode) {
    u32 input[2];
    u8 digest[16];
    u8 table[256];
    u8 md5[88];
    u32 tag;
    input[0] = identity;
    input[1] = key;
    switch (mode) {
    case 0:
        native_crc_init(table, 7);
        tag = native_crc_update(table, input, 8) & 127;
        break;
    case 1:
    default:
        native_md5_init(md5);
        native_md5_update(md5, input, 8);
        native_md5_finish(digest, md5);
        tag = (digest[0] >> 1) & 127;
        break;
    }
    return ((u64)tag << 32) | identity;
}
int saved_sdk_identity_kind_set(void *identity, int kind) {
    int flags = native_sdk_flags(identity);
    flags = flags & ~3;
    flags = flags | kind;
    return native_sdk_flags_set(identity, flags);
}
u64 saved_sdk_profile_code(const u32 *profile) {
    u64 result = 0;
    if (profile[7]) result = saved_identity_code(profile[7], profile[9], 1);
    return result;
}
void saved_sdk_identity_create(void *identity, u32 low, u32 high) {
    native_fill(identity, 0, 12);
    native_sdk_pair_set(identity, low, high);
    saved_sdk_identity_kind_set(identity, 2);
}
