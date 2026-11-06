typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed int s32;
typedef unsigned int u32;
typedef struct {
    u16 action;
    u8 side;
    s8 slot;
    u8 marker;
    u8 unknown;
} Intent;
extern Intent native_data_ov001_02238d1c[3];
extern Intent native_data_ov001_02238d2e[3];
extern u32 native_fn_0203d294(s32 limit);
extern u32 native_fn_ov001_021e6a6c(void *, void *, void *, u16 *, u8 *, s8 *, u32);
extern u32 native_fn_ov001_021e7290(void *, void *, void *, u16 *, u8 *, s8 *);
extern u32 native_fn_ov001_021e741c(void *, void *, void *, u16 *, u8 *, s8 *);
extern u32 native_fn_ov001_021e7484(void *, u32);
void native_ov001_021e7538(s32 index, u8 *own, u8 *opposing, u32 unused) {
    s32 attempts;
    u8 *actor = own + index * 1088;
    Intent *intent;
    u16 action;
    u8 side;
    s8 slot;
    u32 gate;
    u8 fallback_side;
    if (actor[0x31E] == 0) {
        intent = &native_data_ov001_02238d1c[index];
    } else {
        intent = &native_data_ov001_02238d2e[index];
    }
    gate = actor[0x322];
    if (gate == 0) {
        native_fn_ov001_021e6a6c(actor, own, opposing, &action, &side, &slot, 0);
    } else if (gate == 1) {
        attempts = 0;
        for (;;) {
            native_fn_ov001_021e7290(actor, own, opposing, &action, &side, &slot);
            if (native_fn_ov001_021e7484(actor, action) != 0) {
                break;
            }
            attempts++;
            actor[0x35B] = (u8)(actor[0x35B] + 1);
            if (attempts > 32) {
                fallback_side = 0;
                action = 0;
                if (actor[0x31E] == 0) {
                    fallback_side = 1;
                }
                side = fallback_side;
                slot = native_fn_0203d294(3);
                break;
            }
        }
    } else if (gate == 2) {
        native_fn_ov001_021e741c(actor, own, opposing, &action, &side, &slot);
        native_fn_ov001_021e7484(actor, action);
    } else {
        fallback_side = 0;
        action = 0;
        if (actor[0x31E] == 0) {
            fallback_side = 1;
        }
        side = fallback_side;
        slot = native_fn_0203d294(3);
    }
    intent->action = action;
    intent->side = side;
    intent->slot = slot;
}
