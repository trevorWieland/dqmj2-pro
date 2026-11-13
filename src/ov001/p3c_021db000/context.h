/* Shared declarations for the ov001 action-overlay packet that covers the
   accessor rows in 0x021db000-0x021dc000.  External symbols keep the project's
   canonical identity: the trailing eight hex digits are the measured overlay
   address, so the link step binds them to the original symbol. */

typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern s32 native_fn_02044424(u32);
extern s32 native_fn_0203d294(s32);
extern u32 native_fn_022092c0(u8 *, s32, s32, s32, s32);
extern u8 *native_fn_021e81d0(u32, u32);
extern s32 native_fn_021e865c(u32, u32);
extern u32 native_fn_ov001_021d8dec(u32);
extern s32 ov001_record_is_active_021db8d0(u8 *);
extern s32 native_fn_ov001_021dbcf0(u8 *);
extern s32 ov001_record_field_1f2_021dbd30(void);
extern s32 native_fn_ov001_021dbcbc(u8 *);

extern u8 native_data_ov001_022355e4[];   /* four part-table counts */
extern u8 native_data_ov001_022355ec[];   /* fourth part table */
extern u8 native_data_ov001_02236f6c[];   /* first part table */
extern u8 native_data_ov001_022362ac[];   /* second part table */
extern u8 native_data_ov001_02237c2c[];   /* third part table */


