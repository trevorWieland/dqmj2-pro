typedef unsigned int u32;
struct NNSG3dJntAnmResult_;
extern void native_main_0202c6cc(const struct NNSG3dJntAnmResult_ *result);
extern void native_main_0202c788(const struct NNSG3dJntAnmResult_ *result);
extern void native_main_0202cf80(const struct NNSG3dJntAnmResult_ *result);
static u32 words[64];
static u32 length;
void native_fn_0202e434(u32 op, const u32 *args, u32 count) {
    u32 i;
    words[length++] = op;
    words[length++] = count;
    for (i = 0; i < count; ++i) words[length++] = args[i];
}
#ifdef _WIN32
#define J2P_EXPORT __declspec(dllexport)
#else
#define J2P_EXPORT __attribute__((visibility("default")))
#endif
J2P_EXPORT u32 j2p_joint_run(u32 variant, const u32 *input, u32 *output) {
    u32 i;
    const struct NNSG3dJntAnmResult_ *result = (const struct NNSG3dJntAnmResult_ *)input;
    length = 0;
    if (variant == 0) native_main_0202c6cc(result);
    else if (variant == 1) native_main_0202c788(result);
    else native_main_0202cf80(result);
    for (i = 0; i < length; ++i) output[i] = words[i];
    return length;
}
