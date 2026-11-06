typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct {
    void *actor;
    s32 team;
    s32 action;
} TargetPacket;
typedef u32 (*TargetHandler)(TargetPacket *);
extern u32 native_fn_ov001_021dbec8(void *);
extern u32 native_fn_ov001_022182a0(u32, u32, s32);
extern TargetHandler native_fn_ov001_0222be44(u32);
u32 native_ov001_021e686c(void *actor, s32 team, s32 action) {
    TargetPacket packet;
    u32 tier;
    tier = native_fn_ov001_021dbec8(actor);
    packet.actor = actor;
    packet.team = team;
    packet.action = action;
    return (u8)native_fn_ov001_0222be44(native_fn_ov001_022182a0(*((u8 *)actor + 0x31E), tier, action))(&packet);
}
