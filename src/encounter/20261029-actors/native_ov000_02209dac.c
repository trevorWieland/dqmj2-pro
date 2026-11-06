#include "actor_context.h"
extern ActorGlobal native_ov000_data_022385b8;
extern Actor native_ov000_data_02238634[48];
extern int native_ov000_fn_02209c34(void);
extern void native_ov000_fn_02209c68(Actor *actor, s32 mode);
extern void native_ov000_fn_02209d08(Actor *actor);
extern void *native_fn_02008d78(void *destination, int value, u32 bytes);
extern const FieldEnemy *native_fn_020c56b4(s32 enemy);
int native_ov000_02209dac(s32 enemy, s32 x, s32 y, s32 z, s32 angle, u32 group, u8 field, s32 mode)
{
    int slot = -1;
    Actor *actor;
    f32 first;
    f32 second;
    int index;
    if (native_ov000_data_022385b8.selector == (u8)group) {
        slot = native_ov000_fn_02209c34();
        if (slot >= 0) {
            actor = &native_ov000_data_02238634[slot];
            native_fn_02008d78(actor, 0, sizeof(*actor));
            actor->active = 1;
            actor->enemy = enemy;
            actor->field16a = native_fn_020c56b4(enemy)->field2 + 52;
            actor->group = group;
            actor->angle = angle;
            actor->x = x;
            actor->y = y;
            actor->z = z;
            if (mode == 0)
                mode = 0;
            else if (mode == 1)
                mode = 1;
            else if (mode == 2)
                mode = 2;
            native_ov000_fn_02209c68(actor, mode);
            actor->field2c0 = field;
            first = native_fn_020c56b4(enemy)->field12
                ? 0.5f + (f32)(native_fn_020c56b4(enemy)->field12 << 12)
                : (f32)(native_fn_020c56b4(enemy)->field12 << 12) - 0.5f;
            second = native_fn_020c56b4(enemy)->field12
                ? 0.5f + (f32)(native_fn_020c56b4(enemy)->field12 << 12)
                : (f32)(native_fn_020c56b4(enemy)->field12 << 12) - 0.5f;
            actor->radius_squared = ((s64)(s32)second * (s32)first + 0x800) >> 12;
            actor->field2bc = native_fn_020c56b4(enemy)->field14;
            actor->field2c2 = (actor->field2c2 & ~0xF0) | 16;
            actor->field2c3 = 4;
            if (native_fn_020c56b4(enemy)->field7 == 8 || native_fn_020c56b4(enemy)->field6 == 4)
                native_ov000_fn_02209d08(actor);
            for (index = 0; index < 3; index++) {
                actor->array268[index] = -1;
                actor->array26b[index] = -1;
                actor->array26e[index] = -1;
            }
            actor->sentinel1dc = -1;
        }
    }
    return slot;
}
