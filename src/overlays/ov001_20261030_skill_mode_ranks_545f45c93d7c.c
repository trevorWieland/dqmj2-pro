typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
extern u32 native_fn_0207b674(u32, u8 *);
u32 native_ov001_0220e3a8(u8 *actor, s32 primary_mode, s32 secondary_mode, s32 initial_primary, s32 initial_secondary) {
    s32 primary_modifier;
    s32 secondary_modifier;
    s32 secondary_rank;
    s32 primary_rank;

    secondary_rank = initial_secondary;
    primary_modifier = 0;
    secondary_modifier = 0;
    if (secondary_mode == 0) {
        secondary_rank = 8;
    }
    primary_rank = initial_primary;
    if (*(s8 *)(actor + 0x261) != 0) {
        if (primary_rank >= secondary_rank) {
            primary_rank = secondary_rank;
        }
        return (u32) primary_rank;
    }
    if ((s32) native_fn_0207b674(0x76U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        primary_modifier = 1;
        secondary_modifier = 1;
    }
    if ((s32) native_fn_0207b674(0x5AU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 1) {
            primary_modifier = 1;
        } else if (secondary_mode == 1) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x5BU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 2) {
            primary_modifier = 1;
        } else if (secondary_mode == 2) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x5CU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 3) {
            primary_modifier = 1;
        } else if (secondary_mode == 3) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x5DU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 4) {
            primary_modifier = 1;
        } else if (secondary_mode == 4) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x5EU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 5) {
            primary_modifier = 1;
        } else if (secondary_mode == 5) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x5FU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 6) {
            primary_modifier = 1;
        } else if (secondary_mode == 6) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x62U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 7) {
            primary_modifier = 1;
        } else if (secondary_mode == 7) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x63U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 8) {
            primary_modifier = 1;
        } else if (secondary_mode == 8) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x64U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 9) {
            primary_modifier = 1;
        } else if (secondary_mode == 9) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x65U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0xA) {
            primary_modifier = 1;
        } else if (secondary_mode == 0xA) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x66U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0xB) {
            primary_modifier = 1;
        } else if (secondary_mode == 0xB) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x67U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0xC) {
            primary_modifier = 1;
        } else if (secondary_mode == 0xC) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x68U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0xD) {
            primary_modifier = 1;
        } else if (secondary_mode == 0xD) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x69U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0xE) {
            primary_modifier = 1;
        } else if (secondary_mode == 0xE) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x6AU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0xF) {
            primary_modifier = 1;
        } else if (secondary_mode == 0xF) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x6BU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x10) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x10) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x6CU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x11) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x11) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x6DU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x12) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x12) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x6EU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x13) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x13) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x6FU, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x14) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x14) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x70U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x15) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x15) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x71U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x16) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x16) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x72U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x17) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x17) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x74U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x18) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x18) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x75U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x1C) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x1C) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x73U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x19) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x19) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x61U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x1B) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x1B) {
            secondary_modifier = 1;
        }
    }
    if ((s32) native_fn_0207b674(0x60U, *(u8 **)(actor + 0x1E8) + 0x46) > 0) {
        if (primary_mode == 0x1A) {
            primary_modifier = 1;
        } else if (secondary_mode == 0x1A) {
            secondary_modifier = 1;
        }
    }
    if (primary_modifier != 0) {
        if (primary_rank <= 4) {
            primary_rank = 0;
        } else {
            primary_rank = 5;
        }
    }
    if (secondary_modifier != 0) {
        if (secondary_rank <= 4) {
            secondary_rank = 0;
        } else {
            secondary_rank = 5;
        }
    }
    if (primary_rank >= secondary_rank) {
        primary_rank = secondary_rank;
    }
    return (u32) primary_rank;
}
