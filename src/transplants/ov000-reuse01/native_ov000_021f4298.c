typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct { u32 words[8]; } SavedBlock;
typedef struct { u8 prefix[20]; u32 id; u8 before_block[8]; SavedBlock block; u8 tail[68]; } SavedRecord;
typedef struct { u32 tag; u32 id; u8 prefix[38]; s16 species; u8 variant; u8 before_rawb3[130]; u8 rawb3; u8 before_block[104]; SavedBlock block; u8 tail[212]; } RuntimeView;
typedef struct { u32 gold; u8 prefix[28]; RuntimeView party[3]; RuntimeView enemy[3]; RuntimeView reserve[3]; RuntimeView fourth[3]; } RuntimeRoot;
extern RuntimeRoot native_data_ov000_02236ed8;
extern int native_mode(void);
extern SavedRecord *native_record_by_id(u32);
extern void native_gold_set(u32);
extern u32 native_raw153_exchange(u32);
extern void native_bulk_fill(u32, void *, u32);
void saved_runtime_rawb3_set(int first, int second, int third) {
    RuntimeView *views = native_data_ov000_02236ed8.enemy;
    if (native_mode() == 0) {
        views[0].rawb3 = first;
        views[1].rawb3 = second;
        views[2].rawb3 = third;
    } else {
        views[0].rawb3 = 0;
        views[1].rawb3 = 0;
        views[2].rawb3 = 0;
    }
}
void saved_runtime_fourth_markers(int first, int second, int third) {
    switch (native_mode()) {
    case 0:
    case 4:
    case 7:
    case 8:
        native_bulk_fill(0, native_data_ov000_02236ed8.fourth, 1584);
        native_data_ov000_02236ed8.fourth[0].species = -1;
        native_data_ov000_02236ed8.fourth[1].species = -1;
        native_data_ov000_02236ed8.fourth[2].species = -1;
        break;
    case 5:
    case 6: break;
    default:
        native_data_ov000_02236ed8.fourth[0].species = first;
        native_data_ov000_02236ed8.fourth[1].species = second;
        native_data_ov000_02236ed8.fourth[2].species = third;
        break;
    }
}
void saved_runtime_blocks_commit(void) {
    {
        int index = 0;
        RuntimeRoot *root = &native_data_ov000_02236ed8;
        do {
            SavedRecord *record = native_record_by_id(root->party[0].id);
            if (record) record->block = root->party[0].block;
            index++;
            root = (RuntimeRoot *)((u8 *)root + 528);
        } while (index < 3);
    }
    {
        RuntimeRoot *root = &native_data_ov000_02236ed8;
        int index = 0;
        do {
            SavedRecord *record = native_record_by_id(root->reserve[0].id);
            if (record) record->block = root->reserve[0].block;
            index++;
            root = (RuntimeRoot *)((u8 *)root + 528);
        } while (index < 3);
    }
    native_gold_set(native_data_ov000_02236ed8.gold);
    native_raw153_exchange(0);
}
u32 saved_runtime_gold_get(void) {
    return native_data_ov000_02236ed8.gold;
}
u32 native_ov000_021f4298(u32 value) {
    u32 previous = native_data_ov000_02236ed8.gold;
    native_data_ov000_02236ed8.gold = value;
    return previous;
}
