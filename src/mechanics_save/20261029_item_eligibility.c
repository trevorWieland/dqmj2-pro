typedef unsigned char u8;
typedef signed char s8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
#define NULL ((void *)0)
#define FIELD_AT(value, type, offset) (*(type)((s8 *)(value) + (offset)))
extern u32 native_fn_02044e44(s32, s32, s32, s32, s32, s32);
extern u32 native_fn_02044e80(s32, s32, s32, s32, s32, s32);
extern u32 native_fn_02044ebc(s32, s32, s32, s32, s32, s32);
extern u32 native_fn_02044ef8(s32, s32, s32, s32, s32, s32);
extern u32 native_fn_02044f34(s32, s32, s32, s32, s32, s32);
extern u32 native_fn_02044f70(s32, s32, s32, s32, s32, s32);
extern u8 *native_fn_02065d88(int);
extern u32 native_fn_02065e14(const void *, const void *);
extern u32 native_fn_0207c18c(void *, const u8 *);
extern u32 native_fn_0207c1b8(void *, const u8 *);
extern u32 native_fn_0207c2b8(const void *, const u8 *);
extern u32 native_fn_0207c3d8(const void *, const u8 *);
extern u32 native_fn_0207c9e8(const void *);
extern u32 native_fn_ov000_02210bd4(void);
extern u32 native_fn_ov001_021dbcbc(const void *);
extern u32 native_fn_ov001_021dbcf0(const void *);
extern u32 native_fn_ov001_021dbd24(const void *);
extern u32 native_fn_ov001_021dbd30(const void *);
u32 native_main_02065e44(u8 *block, const u8 *bonus, s32 species, s32 variant, const u8 *features, s32 item_id, u8 *live_entity) {
    u32 status_available;
    u32 first_work;
    u32 second_work;
    u32 third_work;
    u32 permitted;
    u8 *status_area;
    u8 kind;
    u8 *entity;
    u32 max_first;
    u32 cap_first;
    u32 cap_second;
    u32 cap_third;
    u32 cap_fourth;
    u32 cap_fifth;
    u32 cap_sixth;
    s32 bonus_first;
    s32 subtype;
    s32 input_variant;
    s32 input_species;

    input_species = species;
    input_variant = variant;
    permitted = 1;
    kind = FIELD_AT(native_fn_02065d88(item_id), u8 *, 0x28);
    subtype = (s32) FIELD_AT(native_fn_02065d88(item_id), u8 *, 0x29);
    native_fn_02065d88(item_id);
    entity = live_entity;
    if (entity != NULL) {
        status_area = entity + 0x22C;
    } else {
        entity = NULL;
        status_area = NULL;
    }
    if (bonus != NULL) {
        first_work = FIELD_AT(bonus, u8 *, 0xC);
        second_work = FIELD_AT(bonus, s16 *, 2);
        bonus_first = (s32) FIELD_AT(bonus, s16 *, 0);
        third_work = FIELD_AT(bonus, u8 *, 0xD);
    } else {
        first_work = 0;
        bonus_first = 0;
        second_work = 0;
        third_work = 0;
    }
    cap_first = native_fn_02044e44(input_species, input_variant, bonus_first, first_work, (s32) second_work, (s32) third_work);
    cap_second = native_fn_02044e80(input_species, input_variant, bonus_first, first_work, (s32) second_work, (s32) third_work);
    cap_third = native_fn_02044ebc(input_species, input_variant, bonus_first, first_work, (s32) second_work, (s32) third_work);
    cap_fourth = native_fn_02044ef8(input_species, input_variant, bonus_first, first_work, (s32) second_work, (s32) third_work);
    cap_fifth = native_fn_02044f34(input_species, input_variant, bonus_first, first_work, (s32) second_work, (s32) third_work);
    cap_sixth = native_fn_02044f70(input_species, input_variant, bonus_first, first_work, (s32) second_work, (s32) third_work);
    if (entity == NULL) {
        if (block != NULL) {
            max_first = native_fn_0207c2b8(block, features);
            first_work = native_fn_0207c18c(block, features);
            third_work = native_fn_0207c3d8(block, features);
            second_work = native_fn_0207c1b8(block, features);
        } else {
            first_work = 0;
            max_first = 0;
            third_work = 0;
            second_work = 0;
        }
    } else {
        max_first = native_fn_ov001_021dbcbc(entity);
        first_work = native_fn_ov001_021dbd24(entity);
        third_work = native_fn_ov001_021dbcf0(entity);
        second_work = native_fn_ov001_021dbd30(entity);
    }
    status_available = native_fn_02065e14(entity, status_area);
    switch ((s32) kind) {
    case 26:
    case 1:
    case 2:
    case 12:
    case 13:
    case 14:
    case 15:
    case 16:
    case 17:
    case 18:
        if (first_work == 0) {
            permitted = 0;
        }
        break;
    }
    switch (kind) {
    default:
        break;
    case 1:
        if (first_work == max_first) {
            permitted = 0;
        }
        break;
    case 2:
        if (second_work == third_work) {
            permitted = 0;
        }
        break;
    case 3:
        if (subtype == 1) {
            if ((s32) first_work >= (s32) max_first) {
                permitted = 0;
            }
        } else if ((s32) first_work > 0) {
            permitted = 0;
        }
        break;
    case 4:
        if (status_available == 0) {
            permitted = 0;
        } else if (FIELD_AT(status_area, s8 *, 6) == 0) {
            permitted = 0;
        }
        break;
    case 5:
        if (status_available == 0) {
            permitted = 0;
        } else if (FIELD_AT(status_area, s8 *, 9) == 0) {
            permitted = 0;
        }
        break;
    case 6:
        if (status_available == 0) {
            permitted = 0;
        } else if ((FIELD_AT(status_area, s8 *, 6) == 0) && (FIELD_AT(status_area, s8 *, 9) == 0) && (FIELD_AT(status_area, s8 *, 0xA) == 0) && (FIELD_AT(status_area, s8 *, 0xB) == 0)) {
            permitted = 0;
        }
        break;
    case 12:
        if (FIELD_AT(block, s16 *, 0x1C) == 0x3E7) {
            permitted = 0;
        }
        break;
    case 13:
        if (FIELD_AT(block, s16 *, 0) == cap_first) {
            permitted = 0;
        }
        break;
    case 14:
        if (FIELD_AT(block, s16 *, 2) == cap_second) {
            permitted = 0;
        }
        break;
    case 15:
        if (FIELD_AT(block, s16 *, 8) == cap_third) {
            permitted = 0;
        }
        break;
    case 16:
        if (FIELD_AT(block, s16 *, 0xA) == cap_fourth) {
            permitted = 0;
        }
        break;
    case 17:
        if (FIELD_AT(block, s16 *, 0xC) == cap_fifth) {
            permitted = 0;
        }
        break;
    case 18:
        if (FIELD_AT(block, s16 *, 0xE) == cap_sixth) {
            permitted = 0;
        }
        break;
    case 24:
        if (native_fn_ov000_02210bd4() == 0) {
            permitted = 0;
        }
        break;
    case 30:
        if (status_available == 0) {
            permitted = 0;
        } else if ((s32) FIELD_AT(FIELD_AT(entity, void **, 0x1E8), s8 *, 0xB0) > 0) {
            permitted = 0;
        }
        break;
    case 31:
        if (status_available == 0) {
            permitted = 0;
        } else if ((FIELD_AT(status_area, s8 *, 0xA) == 0) && (FIELD_AT(status_area, s8 *, 0xB) == 0)) {
            permitted = 0;
        }
        break;
    case 32:
        if (status_available == 0) {
            permitted = 0;
        } else if (FIELD_AT(status_area, s8 *, 0xA) == 0) {
            permitted = 0;
        }
        break;
    case 33:
        if (status_available == 0) {
            permitted = 0;
        } else if (FIELD_AT(status_area, s8 *, 0xB) == 0) {
            permitted = 0;
        }
        break;
    case 7:
    case 8:
    case 9:
    case 10:
    case 23:
    case 34:
    case 35:
    case 36:
    case 37:
    case 38:
    case 39:
    case 40:
    case 41:
    case 42:
    case 43:
    case 44:
    case 45:
    case 46:
    case 47:
        if (status_available == 0) {
            permitted = 0;
        }
        break;
    case 19:
    case 20:
    case 21:
    case 22:
    case 25:
    case 26:
    case 27:
    case 28:
    case 29:
        permitted = 0;
        break;
    case 48:
        if (native_fn_0207c9e8(block) == 0) {
            permitted = 0;
        }
        break;
    }
    return permitted;
}
