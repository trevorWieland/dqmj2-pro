typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 tag; u32 id; u8 tail[520]; } RuntimeView;
typedef struct { u8 prefix[32]; RuntimeView party[3]; RuntimeView enemy[3]; RuntimeView reserve[3]; RuntimeView fourth[3]; } RuntimeRoot;
extern RuntimeRoot native_runtime_root;
extern void native_copy(const void *, void *, u32);
RuntimeView *saved_runtime_view_find(int group, u32 id) {
    RuntimeView *found = 0;
    if (!(group & 1)) {
        {
            int index = 0;
            RuntimeRoot *root = &native_runtime_root;
            do {
                if (id == root->party[0].id) {
                    found = &native_runtime_root.party[index];
                    break;
                }
                index++;
                root = (RuntimeRoot *)((u8 *)root + 528);
            } while (index < 3);
        }
        if (found) return found;
        {
            RuntimeRoot *root = &native_runtime_root;
            int index = 0;
            do {
                if (id == root->reserve[0].id) {
                    found = &native_runtime_root.reserve[index];
                    break;
                }
                index++;
                root = (RuntimeRoot *)((u8 *)root + 528);
            } while (index < 3);
        }
    } else {
        {
            RuntimeRoot *root = &native_runtime_root;
            int index = 0;
            do {
                if (id == root->enemy[0].id) {
                    found = &native_runtime_root.enemy[index];
                    break;
                }
                index++;
                root = (RuntimeRoot *)((u8 *)root + 528);
            } while (index < 3);
        }
        if (found) return found;
        {
            RuntimeRoot *root = &native_runtime_root;
            int index = 0;
            do {
                if (id == root->fourth[0].id) {
                    found = &native_runtime_root.fourth[index];
                    break;
                }
                index++;
                root = (RuntimeRoot *)((u8 *)root + 528);
            } while (index < 3);
        }
    }
    return found;
}
int saved_runtime_view_swap(int group, int index, u32 id) {
    RuntimeView temporary;
    RuntimeView *selected;
    RuntimeView *found;
    if (group == 0) selected = &native_runtime_root.party[index];
    else if (group == 2) selected = &native_runtime_root.reserve[index];
    else if (group == 1) selected = &native_runtime_root.enemy[index];
    else selected = &native_runtime_root.fourth[index];
    found = saved_runtime_view_find(group, id);
    if (!found) return 0;
    native_copy(selected, &temporary, 528);
    native_copy(found, selected, 528);
    native_copy(&temporary, found, 528);
    return 1;
}
