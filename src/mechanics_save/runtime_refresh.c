typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct { u8 prefix[46]; s16 species; u8 variant; u8 before_name[133]; u8 name[20]; u8 tail[326]; } RuntimeView;
typedef struct { u32 gold; u8 prefix[28]; RuntimeView views[3]; } RuntimeRoot;
extern RuntimeRoot native_runtime_root;
extern int native_mode(void);
extern void *native_party_record(int);
extern void *native_side_record(int);
extern int native_side_count(void);
extern u32 native_gold(void);
extern int native_runtime_view(RuntimeView *, void *, int);
extern u8 *native_name_build(u8 *, int, int);
extern void native_noop(void);
extern void native_bulk_fill(u32, void *, u32);
void saved_runtime_views_refresh(int first, int second, int third) {
    switch (native_mode()) {
    case 0:
    case 3:
    case 5:
    case 6:
    case 7:
    case 8: {
        int index = 0;
        RuntimeView *view = native_runtime_root.views;
        do {
            native_runtime_view(view, native_party_record(index), 0);
            index++;
            view++;
        } while (index < 3);
        native_runtime_root.gold = native_gold();
        break;
    }
    case 4: {
        int count = native_side_count();
        RuntimeView *view;
        int index;
        native_bulk_fill(0, native_runtime_root.views, 1584);
        native_runtime_root.views[0].species = -1;
        native_runtime_root.views[1].species = -1;
        native_runtime_root.views[2].species = -1;
        index = 0;
        if (count > 0) {
            view = native_runtime_root.views;
            do {
            native_runtime_view(view, native_side_record(index), 0);
            index++;
            view++;
            } while (index < count);
        }
        native_runtime_root.gold = 0;
        break;
    }
    case 1: {
        native_runtime_root.views[0].species = first;
        native_runtime_root.views[1].species = second;
        native_runtime_root.views[2].species = third;
        {
        RuntimeView *view = native_runtime_root.views;
        int index = 0;
        do {
            if (view->species >= 0) native_name_build(view->name, view->species, view->variant);
            index++;
            view++;
        } while (index < 3);
        }
        native_noop();
        break;
    }
    default: break;
    }
}
