typedef unsigned char u8;
typedef signed char s8;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_ov001_021dbec8();
extern u32 native_fn_ov001_02218168();
extern u32 native_fn_ov001_02218178();
extern u32 native_fn_ov001_02218224();
extern u32 native_fn_ov001_02223f10();
typedef struct {
    s32 actor;
    s32 arg1;
    s32 arg2;
    s32 key;
    s32 zero;
    s32 arg5;
    s32 override;
} RewardConditionContext;
u32 native_ov001_021e6764(s32 arg0, s32 arg1, s32 arg2, s32 arg3, u32 arg4, s32 arg5) {
    s8 temp_r0;
    s8 temp_r1;
    u32 entry;
    s32 index;
    u32 value;
    RewardConditionContext context;
    s32 first;
    s32 last;

    context.arg1 = arg1;
    context.arg2 = arg2;
    context.actor = arg0;
    context.key = arg3;
    context.zero = 0;
    context.arg5 = arg5;
    value = arg4;
    native_fn_ov001_02218178(arg3, &first, &last);
    index = first;
    if (index <= last) {
loop_2:
        entry = native_fn_ov001_02218168(index);
        if (native_fn_ov001_02218224(M2C_FIELD(entry, u16 *, 0), (u8) (1 << native_fn_ov001_021dbec8(arg0))) != 0) {
            context.override = -1;
            if (((s32 (*)(RewardConditionContext *)) native_fn_ov001_02223f10(M2C_FIELD(entry, u16 *, 0)))(&context) != 0) {
                temp_r1 = M2C_FIELD(entry, s8 *, 2);
                if (temp_r1 == -0x80) {
                    return -1U;
                }
                if (context.override < 0) {
                    value += temp_r1;
                } else {
                    value += context.override;
                }
                goto block_13;
            }
            temp_r0 = M2C_FIELD(entry, s8 *, 3);
            if (temp_r0 == -0x80) {
                return -1U;
            }
            value += temp_r0;
            goto block_13;
        }
block_13:
        index += 1;
        if (index > last) {
            
            goto done;
        }
        goto loop_2;
    }
done:
    return value;
}
