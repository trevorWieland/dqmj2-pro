typedef unsigned int u32;
typedef signed int s32;
typedef struct Context { u32 state; u32 interruptMode; } Context;
typedef char context_prefix_size[(sizeof(Context)==8)?1:-1];
extern s32 native_host_arm7_arm_037fbb78(u32);
extern u32 native_host_arm7_arm_037fdd14(u32);
u32 native_arm7_wram_03806390(u32 owner, Context *context) {
    if (context->state == 0) native_host_arm7_arm_037fbb78(owner);
    return native_host_arm7_arm_037fdd14(context->interruptMode);
}
