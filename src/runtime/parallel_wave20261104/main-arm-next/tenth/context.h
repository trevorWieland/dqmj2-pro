typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef struct PlayerFlags { s32 bit0:1; s32 bit1:1; s32 bit2:1; s32 bit3:1; u32 remaining:28; } PlayerFlags;
typedef struct Player { u8 opaque00[0xc4]; u16 ratec4; u8 opaquec6[0x22]; u8 timerDatae8[0x28]; PlayerFlags flags110; u32 field114; u32 field118; u8 opaque11c[0x38]; s32 index154; s32 index158; s32 current15c; u32 counter160; u8 opaque164[0x10]; } Player;
typedef struct PlayerHandle { Player *player; } PlayerHandle;
extern void native_fn_0203a4fc(Player *, u32);
extern void native_fn_0203b8dc(Player *, u32, u32);
extern void native_fn_020379c4(void *, u32, u32);
extern u64 native_fn_020260dc(u64, u64);
extern u32 native_fn_02039f2c(PlayerHandle *, u32, u32, u32, u32);
extern void native_fn_02039fa4(PlayerHandle *);
typedef char FlagsWidth[(sizeof(PlayerFlags) == 4) ? 1 : -1];
typedef char TimerOffset[((u32)&((Player *)0)->timerDatae8 == 0xe8) ? 1 : -1];
typedef char FlagsOffset[((u32)&((Player *)0)->flags110 == 0x110) ? 1 : -1];
typedef char CounterOffset[((u32)&((Player *)0)->counter160 == 0x160) ? 1 : -1];
typedef char PlayerStride[(sizeof(Player) == 0x174) ? 1 : -1];
static inline Player *playerHandleValue(const PlayerHandle *handle)
{
    return handle->player;
}
