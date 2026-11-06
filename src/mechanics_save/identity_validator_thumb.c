typedef unsigned int u32;
typedef unsigned long long u64;
extern u64 native_identity_code(u32, u32, int);
int saved_identity_code_valid(u64 code, u32 key, int mode) {
    u64 identity = code & 0xffffffffULL;
    if ((int)identity <= 0) return (u32)(code & 0);
    {
        if (code == native_identity_code((u32)identity, key, mode)) return 1;
        return 0;
    }
}
