typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef struct { u8 prefix[46]; s16 species; u8 tail[480]; } RuntimeView;
typedef struct { u8 prefix[128]; RuntimeView views[3]; } RuntimeRoot;
extern RuntimeRoot native_runtime_root;
extern int native_mode(void);
extern void *native_reserve_record(int);
extern int native_runtime_view(RuntimeView *, void *, int);
extern void native_bulk_fill(u32, void *, u32);
void saved_reserve_views_refresh(int first, int second, int third) {
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
            native_runtime_view(view, native_reserve_record(index), 0);
            index++;
            view++;
        } while (index < 3);
        break;
    }
    case 4:
        native_bulk_fill(0, native_runtime_root.views, 1584);
        native_runtime_root.views[0].species = -1;
        native_runtime_root.views[1].species = -1;
        native_runtime_root.views[2].species = -1;
        break;
    case 1:
        native_runtime_root.views[0].species = first;
        native_runtime_root.views[1].species = second;
        native_runtime_root.views[2].species = third;
        break;
    default: break;
    }
}
