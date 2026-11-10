/* Shared declarations for the ov001 action-overlay packet that starts at
   0x021d732c.  Every external symbol keeps the project's canonical identity in
   its name: the trailing eight hex digits are the measured overlay address, so
   the link step can bind it to the original symbol.  Globals are addressed as
   byte blocks because only the individual offsets listed here are measured. */

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef signed long long s64;

/* Three s32 cells copied as one unit by the kind-0 position paths. */
typedef struct {
    s32 x;
    s32 y;
    s32 z;
} Vector3;

/* Battle-overlay globals: a 0x176C-byte state block at 0x0222fd50 whose word at
   0x4C is the currently selected roster slot (signed halfword, -1 = none) and
   whose byte at 0x4E is the "selection change pending" gate. */
typedef struct {
    u8 unknown_0[0x4C];
    s16 field_4c;
    u8 field_4e;
} Record_native_data_ov001_0222fd50;

extern Record_native_data_ov001_0222fd50 native_data_ov001_0222fd50;

/* Roster/actor records: 0x31 slots of 0x78 bytes.  Byte 0 is the occupied flag,
   byte 1 the record kind (0/1/2); the kind-specific state starts at +0x1C. */
extern u8 native_data_ov001_0222fda0[];

/* Screen/asset layer state blocks, addressed by their measured overlay address. */
extern u8 native_data_ov001_022316bc[];   /* +0x60: bound asset id (s16); +92: draw limit */
extern u8 native_data_ov001_022315bc[];   /* +92: vertex limit (u16) */
extern u8 native_data_ov001_02235530[];   /* 84-byte mixer block: 4 slots of 20 */
extern u8 native_data_ov001_02235534[];   /* first mixer slot */
extern u8 native_data_ov001_0222ea30[];   /* 8-byte stride u32 selector table */
extern u8 native_data_ov001_0222ea34[];   /* 8-byte stride u32 selector table */
extern u8 native_data_ov001_02232b90[];   /* 9-byte stride byte table */
extern u8 native_data_ov001_02232b91[];   /* same table, +1 view */
extern u8 native_data_ov001_0222fd2c[];   /* 12-byte staging vector */
extern u8 native_data_ov001_0222fd38[];   /* second 12-byte staging vector */
extern u8 native_data_ov001_02233500[];   /* 16-byte packed 2-bit rows */
extern u8 native_data_ov001_02232c20[];   /* 8-byte packed bit rows */

/* Platform and overlay services. */
extern u32 native_fn_0202a1e0(u32);
extern u32 native_fn_0202a260(void);
extern u32 native_fn_0202a280(void);
extern u32 native_fn_020445e4(s32, s32, void *, s32);
extern u32 native_fn_020448b8(void *);
extern u32 native_fn_02044978(void *, s32, s32, s32);
extern u32 native_fn_02044988(void *, ...);
extern s32 native_fn_02008d78(void *, s32, u32);
extern u8 *native_fn_0202859c(s32, s32);
extern u8 *native_fn_020285c8(s32, s32);
extern s32 native_fn_02044cdc(u32);
extern u32 native_fn_ov001_021d768c(u32);
extern u32 native_fn_ov001_021d77b0(s16, s32);
extern s32 native_fn_ov001_021db438(s32, s32);
extern s32 native_fn_ov001_021db8d0(void *);
extern s32 native_fn_ov001_021dbaac(void *);
extern s32 native_fn_ov001_021d94cc(u32, u32);
extern s32 native_fn_ov001_021d92f8(u32, s32);
extern s32 native_fn_ov001_021eeb70(s32);
extern s32 native_fn_020286e8(void *, s32);
extern s32 native_fn_0201d444(void *, u32, u32);
extern s32 native_fn_0202a8e0(void *);
extern s32 native_fn_0202a818(void *, u32, s32);
extern s32 native_fn_02040e0c(u32, u32, s32);
extern s32 native_fn_02040fb0(u32, s32, s32);
extern s32 native_fn_0204106c(u32, u32, s32);
extern s32 native_fn_020410f0(u32, s32);
extern s32 native_fn_02029284(u32, s32, s32, u32, u32);
extern s32 native_fn_0203cc3c(void *, s32);
extern s32 native_fn_0203cf9c(s32, s32);
extern u32 native_fn_ov001_021d8ce0(u32);



