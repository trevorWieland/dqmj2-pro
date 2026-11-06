typedef unsigned int u32;
typedef unsigned long long u64;
extern int native_identity_kind(const u32 *);
extern u32 native_identity_word1(const u32 *);
extern u32 native_identity_word2(const u32 *);
extern u64 native_identity_login(const u32 *);
extern u64 native_identity_pair(const u32 *);
int saved_identity_equal(const u32 *first, const u32 *second) {
    int kind = native_identity_kind(first);
    if (kind != native_identity_kind(second)) return 0;
    if (kind == 3) return native_identity_word1(first) == native_identity_word1(second);
    if (kind == 1) return native_identity_login(first) == native_identity_login(second) && native_identity_word2(first) == native_identity_word2(second);
    if (kind == 2) return native_identity_pair(first) == native_identity_pair(second);
    return 0;
}
