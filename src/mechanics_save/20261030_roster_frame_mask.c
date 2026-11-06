typedef unsigned char u8;
typedef signed char s8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct Widget {
    u8 prefix[0x7C];
    u32 flags;
} Widget;
typedef struct Slot {
    u8 padding;
    u8 count;
    s8 first;
    u8 tail[21];
} Slot;
extern Widget *native_data_021c4b74[];
extern Widget *native_data_021c4afc[];
extern u8 native_data_021c4bf9[];
extern s8 native_data_021c4bfa[];
extern Slot native_data_021c4bf8[];
void native_main_0206d114(s32 sprite, s32 enabled) {
    if (enabled != 0) {
        s8 index;
        Slot *slot;
        native_data_021c4b74[sprite]->flags |= 2;
        index = native_data_021c4bfa[sprite * 24];
        if (index < (s8)(index + native_data_021c4bf9[sprite * 24])) {
            slot = &native_data_021c4bf8[sprite];
            do {
                native_data_021c4afc[index]->flags |= 2;
                index++;
            } while (index < (s8)(slot->first + slot->count));
        }
    } else {
        Slot *slot;
        s8 index;
        native_data_021c4b74[sprite]->flags &= ~2U;
        index = native_data_021c4bfa[sprite * 24];
        if (index < (s8)(index + native_data_021c4bf9[sprite * 24])) {
            slot = &native_data_021c4bf8[sprite];
            do {
                native_data_021c4afc[index]->flags &= ~2U;
                index++;
            } while (index < (s8)(slot->first + slot->count));
        }
    }
}
