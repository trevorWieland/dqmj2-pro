/* Shared declarations for the ov001 action-overlay packet that covers the
   accessor rows in 0x021da544-0x021dacd0.  External symbols keep the project's
   canonical identity: the trailing eight hex digits are the measured overlay
   address, so the link step binds them to the original symbol. */

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

typedef struct {
    s32 x;
    s32 y;
    s32 z;
} Vector3;

/* The 0x35D status byte: a raw byte view plus two single-bit gates. */
typedef union {
    u8 raw;
    struct {
        u8 disabled : 1;
        u8 blocked : 1;
        u8 spare : 6;
    } bits;
} ActorStatus;

extern u32 native_fn_022094bc();
extern s32 native_fn_02044cdc(s32);
extern s32 native_fn_022025a4(u32, u32, s32);
extern s32 native_fn_021e29e8(void);
extern s32 native_fn_022177e0(void);
extern s32 native_fn_021f5d6c(void);
extern s32 native_fn_02042b3c(u8 *, void *);
extern s32 native_fn_ov001_021da480(u32, s32);
extern s32 native_fn_ov001_021d9494(u8 *, u32, s32);
extern s32 native_fn_ov001_021d95b0(u8 *);
extern s32 native_fn_ov001_021d96d4(u8 *, u32);
extern s32 native_fn_ov001_021db410(u8 *, s32);
extern u32 ov001_side_slot_record_021db438(u32, u32);
extern u32 native_fn_ov001_021d8dec(u32);
extern s32 native_fn_ov001_021dc940(u8 *, s32);
extern s32 native_fn_ov001_021e865c(u32, u32);
extern s32 ov001_effect_resource_create_021eec7c(u32, u8 *, s32);
extern s32 native_fn_ov001_021f949c(u32, u32);

