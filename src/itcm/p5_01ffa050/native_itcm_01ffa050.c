typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;

extern u8 native_data_021cebe0[];
extern u8 native_data_021cec40[];
extern u8 native_data_021cec54[];
extern u8 native_data_021cecf4[];

extern u32 native_fn_020633b0(void);
extern void native_fn_02083fac(u32, u32);
extern u32 native_fn_02083fe0(void);
extern u32 native_fn_02083fec(void);
extern u32 native_fn_02083ff8(void);
extern u32 native_fn_02084048(u32);
extern u32 native_fn_02084100(void);
extern u32 native_fn_0202a37c(u32, u32, u32);
extern void native_fn_02084004(void);
extern void native_fn_02084010(void);
extern void native_fn_0208401c(void);
extern void native_fn_02084028(void);
extern void native_fn_02084080(void);
extern void native_fn_020840e8(u32);
extern void native_fn_02084120(void);
extern void native_fn_02084134(u32);
extern void native_fn_02008d78(u32, u32, u32);
extern void native_fn_02008e0c(u32, u32, u32);
extern void native_fn_020081fc(u32);
extern void native_fn_020844fc(u32);
extern void native_fn_0204bb08(void);
extern void native_fn_01ffa02c(void);
extern void native_fn_01ffa204(void);

#define FIELD(base, type, offset) (*(type *)((u8 *)(base) + (offset)))

/* One animation row: three flags sit inside a 0x170-byte stride. */
typedef struct {
    u8 pad0[0x165];
    s8 column;
    u8 enabled;
    u8 pad1[0x7];
    s8 mirror;
    u8 pad2[0x1];
} AnimRow;

/* One-time scene bring-up: size the shared context from the boot mode byte,
   allocate the five work buffers, install the command lists and clear the eight
   animation rows before handing control to the steady-state tick. */
void native_itcm_01ffa050(void) {
    AnimRow *slot;
    s32 mode = native_fn_020633b0();
    s32 row;
    s8 value;

    if (native_data_021cebe0[5] == 0) {
        native_fn_02083fac(7, 0x3c);
    } else {
        native_fn_02083fac(1, 0x54);
    }
    FIELD(native_data_021cebe0, u32, 0x18) = native_fn_0202a37c(8, native_fn_02083fe0(), 0x20);
    native_fn_02084004();
    FIELD(native_data_021cebe0, u32, 0x14) = native_fn_0202a37c(8, native_fn_02083fec(), 0x20);
    native_fn_02084010();
    FIELD(native_data_021cebe0, u32, 0x34) = native_fn_0202a37c(8, native_fn_02083ff8(), 0x20);
    native_fn_0208401c();
    native_fn_01ffa02c();
    native_fn_02084028();
    FIELD(native_data_021cebe0, u32, 0x2c) = native_fn_0202a37c(8, native_fn_02084048(1), 0x20);
    native_fn_02084080();
    native_fn_020840e8(3);
    FIELD(native_data_021cebe0, u32, 0x10) = native_fn_0202a37c(8, native_fn_02084100(), 4);
    native_fn_02084120();
    native_fn_02008d78((u32)native_data_021cec40, 0, 0x20);
    native_fn_02008e0c(mode, (u32)(void *)native_data_021cec40, 0x14);
    native_fn_020081fc((u32)native_data_021cec54);
    native_fn_020844fc(0x1566);
    native_data_021cebe0[6] = 0;
    native_fn_02084134(1);
    native_fn_02008d78(FIELD(native_data_021cebe0, u32, 0x2c), 0, native_fn_02084048(1));
    slot = (AnimRow *)native_data_021cecf4;
    for (row = 0; row < 8; row++) {
        value = (s8)row;
        slot[row].column = value;
        slot[row].enabled = 0;
        slot[row].mirror = value;
    }
    native_fn_01ffa204();
    /* Clear the run-state word and the scene-select byte in one go. */
    {
        u32 *state = (u32 *)native_data_021cebe0;
        state[0xc] = 0;
        ((u8 *)state)[1] = 0;
    }
    native_fn_0204bb08();
}
