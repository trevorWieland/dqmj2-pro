typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct { u8 prefix[20]; u32 id; s16 species; u8 variant; u8 middle[22]; u8 equipment; u8 tail[82]; } SavedRecord;
extern SavedRecord native_saved_records[];
extern SavedRecord *saved_party_record(int);
extern SavedRecord *saved_reserve_record(int);
extern int saved_inventory_count_get(int);
int saved_roster_species_count(int species, int variant) {
    int index;
    int count;
    SavedRecord *record;
    count = 0;
    index = 0;
    record = native_saved_records;
    do {
        if (record->id && record->species == species && (variant == 4 || record->variant == variant)) count++;
        index++;
        record++;
    } while (index < 100);
    return count;
}
int saved_reserve_species_count(int species, int variant) {
    int count = 0;
    int index = 0;
    do {
        SavedRecord *record = saved_reserve_record(index);
        if (record && record->species == species && (variant == 4 || record->variant == variant)) count++;
        index++;
    } while (index < 3);
    return count;
}
int saved_equipped_item_count(int item) {
    int count = 0;
    int index = 0;
    do {
        SavedRecord *record = saved_party_record(index);
        if (record && record->equipment == item) count++;
        index++;
    } while (index < 3);
    index = 0;
    do {
        SavedRecord *record = saved_reserve_record(index);
        if (record && record->equipment == item) count++;
        index++;
    } while (index < 3);
    return count;
}
int saved_inventory_unequipped_raw(int item) {
    int quantity = saved_inventory_count_get(item);
    return quantity - saved_equipped_item_count(item);
}
