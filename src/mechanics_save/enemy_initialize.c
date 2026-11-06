typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { s16 values[16]; } SavedBlock;
typedef struct { u8 prefix[20]; u32 id; u8 tail[108]; } SavedRecord;
typedef struct { u8 prefix[48]; SavedRecord records[3]; } SavedGroup;
typedef struct { u32 tag; u32 id; u8 prefix[38]; s16 species; u8 variant; u8 before_raw32; u16 raw32; u8 before_features[22]; u8 features[64]; u8 projection[32]; u8 rawaa; u8 before_name[11]; u8 name[20]; u8 before_block[82]; SavedBlock block; u8 tail[212]; } RuntimeView;
typedef struct { u32 gold; u8 prefix[28]; RuntimeView party[3]; RuntimeView enemy[3]; } RuntimeRoot;
extern RuntimeRoot native_runtime_root;
extern int native_mode(void);
extern int native_active_group(void);
extern SavedRecord *native_group_record(int, int);
extern SavedGroup *native_saved_group(int);
extern void native_bulk_fill(u32, void *, u32);
extern int native_runtime_view(RuntimeView *, SavedRecord *, int);
extern u32 native_derive24(SavedBlock *, const u8 *);
extern u32 native_derive26(SavedBlock *, const u8 *);
extern u8 *native_name_build(u8 *, int, int);
extern u32 native_random(int);
extern void *native_battle_skills(int);
extern int native_feature_collect(int, int, void *, u8 *);
extern int native_action_filter(void *, const u8 *, u32 *);
extern void native_projection(int, int, const u8 *, u8 *);
void saved_enemy_views_initialize(int first, int second, int third) {
    RuntimeView *views = native_runtime_root.enemy;
    int mode = native_mode();
    if (mode == 0 || mode == 2 || mode == 8) {
        views[0].tag = (s16)first;
        views[1].tag = (s16)second;
        views[2].tag = (s16)third;
        native_runtime_root.prefix[12] = 0;
        return;
    }
    if (mode == 4) {
        int extra;
        RuntimeView *view;
        int group = native_active_group();
        int index;
        native_bulk_fill(0, views, 1584);
        views[0].species = -1;
        views[1].species = -1;
        views[2].species = -1;
        index = 0;
        view = native_runtime_root.enemy;
        extra = 0;
        do {
            SavedRecord *record = native_group_record(group, index);
            if (record->id) {
                native_runtime_view(view, record, extra);
                view++;
            }
            index++;
        } while (index < 3);
        native_runtime_root.prefix[12] = 0;
        return;
    }
    if (mode == 5 || mode == 6) { } else {
    if (mode == 7) {
        int extra;
        SavedRecord *record;
        RuntimeView *view;
        u8 *features;
        SavedBlock *block;
        RuntimeRoot *root;
        int index;
        SavedGroup *group = native_saved_group(first);
        features = native_runtime_root.enemy[0].features;
        block = &native_runtime_root.enemy[0].block;
        root = &native_runtime_root;
        view = native_runtime_root.enemy;
        views[0].species = -1;
        views[1].species = -1;
        views[2].species = -1;
        record = group->records;
        index = 0;
        extra = 1;
        do {
            if (record->id) {
                native_runtime_view(view, record, extra);
                root->enemy[0].block.values[2] = native_derive24(block, features);
                root->enemy[0].block.values[3] = native_derive26(block, features);
                view++;
                features += 528;
                block = (SavedBlock *)((u8 *)block + 528);
                root = (RuntimeRoot *)((u8 *)root + 528);
            }
            index++;
            record++;
        } while (index < 3);
        return;
    }
    if (mode != 1) return;
    views[0].species = first;
    views[1].species = second;
    views[2].species = third;
    views[0].variant = 0;
    views[1].variant = 0;
    views[2].variant = 0;
    views[0].id = 2000;
    views[1].id = 2001;
    views[2].id = 2002;
    {
        RuntimeRoot *root = &native_runtime_root;
        u8 *name = native_runtime_root.party[0].name;
        int index = 0;
        do {
            if (root->party[0].species >= 0) native_name_build(name, root->party[0].species, root->party[0].variant);
            index++;
            root = (RuntimeRoot *)((u8 *)root + 528);
            name += 528;
        } while (index < 3);
    }
    native_runtime_root.prefix[12] = 0;
    views[0].block.values[0] = 400;
    views[0].block.values[1] = 100;
    views[0].block.values[4] = 50;
    views[0].block.values[5] = 100;
    views[0].block.values[6] = 108;
    views[0].block.values[7] = 54;
    views[0].block.values[2] = 100;
    views[0].block.values[3] = 100;
    views[0].raw32 = (u8)(native_random(10) + 1);
    views[0].rawaa = native_random(10) + 1;
    views[1].block.values[0] = 600;
    views[1].block.values[1] = 100;
    views[1].block.values[4] = 50;
    views[1].block.values[5] = 100;
    views[1].block.values[6] = 107;
    views[1].block.values[7] = 53;
    views[1].block.values[2] = 200;
    views[1].block.values[3] = 100;
    views[1].raw32 = (u8)(native_random(10) + 1);
    views[1].rawaa = native_random(10) + 1;
    views[2].block.values[0] = 600;
    views[2].block.values[1] = 100;
    views[2].block.values[4] = 50;
    views[2].block.values[5] = 100;
    views[2].block.values[6] = 107;
    views[2].block.values[7] = 53;
    views[2].block.values[2] = 300;
    views[2].block.values[3] = 100;
    views[2].raw32 = (u8)(native_random(10) + 1);
    views[2].rawaa = native_random(10) + 1;
    {
        int projection_variant = 0;
        int collect_variant = 0;
        RuntimeView *view = native_runtime_root.enemy;
        int index = 0;
        do {
            if (view->species != -1) {
                native_feature_collect(view->species, collect_variant, native_battle_skills(index), view->features);
                native_action_filter(native_battle_skills(index), view->features, (u32 *)((u8 *)view + 12));
                native_projection(view->species, projection_variant, view->features, view->projection);
            }
            index++;
            view++;
        } while (index < 3);
    }
    }
}
