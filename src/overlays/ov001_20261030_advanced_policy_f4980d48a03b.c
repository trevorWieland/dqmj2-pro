typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
#define M2C_FIELD(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_0203d294();
extern u32 native_fn_0207afec();
extern u32 native_fn_ov001_021e2b88();
extern u32 native_fn_ov001_021e6db4();
extern u32 native_fn_ov001_021e6e40();
extern u32 native_fn_ov001_021e7484();
u32 native_ov001_021e6fd8(void *actor, s32 ownTeam, s32 opponentTeam, u32 policy) {
    u8 phaseParity;
    u8 phaseQuarter;
    s32 retry;
    u32 drawPair;
    u32 drawQuarterPair;
    u8 phaseSix;
    s32 quarter;
    s32 skillIndex;
    u8 phaseThree;
    u8 action;
    s32 triedCount;
    s32 nextIndex;
    s32 attempts;
    s32 rejected[5];
    u32 savedPolicy;
    s32 savedOpponentTeam;
    s32 savedOwnTeam;

    action = 0;
    savedOwnTeam = ownTeam;
    savedOpponentTeam = opponentTeam;
    savedPolicy = policy;
    attempts = 0;
loop_1:
    switch (savedPolicy) {
    default:
        break;
    case 4:
        phaseSix = M2C_FIELD(actor, u8 *, 0x35B);
        skillIndex = phaseSix % 6;
        action = M2C_FIELD((M2C_FIELD(actor, s32 *, 0x1E8) + skillIndex), u8 *, 8);
        break;
    case 5:
        drawPair = native_fn_0203d294(2);
        phaseThree = M2C_FIELD(actor, u8 *, 0x35B);
        action = M2C_FIELD((drawPair + (M2C_FIELD(actor, s32 *, 0x1E8) + (phaseThree % 3) * 2)), u8 *, 8);
        break;
    case 6:
        phaseParity = M2C_FIELD(actor, u8 *, 0x35B);
        skillIndex = 0;
        if (phaseParity % 2 != 0) {
            skillIndex = native_fn_0203d294(5) + 1;
        }
        action = M2C_FIELD((M2C_FIELD(actor, s32 *, 0x1E8) + skillIndex), u8 *, 8);
        if (native_fn_ov001_021e7484(actor, action) == 0) {
            if (skillIndex != 0) {
                M2C_FIELD((u32)rejected, s32 *, 0) = 0;
                M2C_FIELD((u32)rejected, s32 *, 4) = 0;
                M2C_FIELD((u32)rejected, s32 *, 8) = 0;
                M2C_FIELD((u32)rejected, s32 *, 0xC) = 0;
                M2C_FIELD((u32)rejected, s32 *, 0x10) = 0;
                triedCount = 1;
                M2C_FIELD(rejected + skillIndex, s32 *, -4) = 1;
loop_19:
                nextIndex = native_fn_0203d294(5) + 1;
                if (M2C_FIELD(rejected + nextIndex, s32 *, -4) == 0) {
                    action = M2C_FIELD((M2C_FIELD(actor, s32 *, 0x1E8) + nextIndex), u8 *, 8);
                    if (native_fn_ov001_021e7484(actor, action) == 0) {
                        M2C_FIELD((s32)rejected + nextIndex * 4, s32 *, -4) = 1;
                        triedCount += 1;
                        goto block_22;
                    }
                } else {
block_22:
                    if (triedCount < 5) {
                        goto loop_19;
                    }
                }
                if (triedCount >= 5) {
                    action = 0;
                }
            } else {
                action = 0;
            }
        }
        break;
    case 7:
        phaseQuarter = M2C_FIELD(actor, u8 *, 0x35B);
        quarter = phaseQuarter % 4;
        if (quarter < 2) {
            drawQuarterPair = native_fn_0203d294(2);
            action = M2C_FIELD((drawQuarterPair + (M2C_FIELD(actor, s32 *, 0x1E8) + (quarter * 2))), u8 *, 8);
        } else {
            action = M2C_FIELD((M2C_FIELD(actor, s32 *, 0x1E8) + quarter), u8 *, 0xA);
        }
        break;
    }
    if (native_fn_ov001_021e6e40(actor, savedOwnTeam, savedOpponentTeam, action) != 0) {
        action = 0;
    }
    if ((((s32) native_fn_ov001_021e2b88() >= 2) && (M2C_FIELD((void *) native_fn_0207afec(action), s8 *, 0x26) != 0)) || (native_fn_ov001_021e6db4(M2C_FIELD(actor, u8 *, 0x31E), action, M2C_FIELD(actor, u8 *, 0x31F)) != 0)) {
        retry = 1;
        M2C_FIELD(actor, u8 *, 0x35B) = (u8) (M2C_FIELD(actor, u8 *, 0x35B) + 1);
    } else {
        retry = 0;
    }
    attempts += 1;
    if ((retry != 0) && (attempts <= 0xC)) {
        goto loop_1;
    }
    if (attempts > 0xC) {
        action = 0;
    }
    return (u32) action;
}
