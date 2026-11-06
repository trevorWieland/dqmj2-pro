#include "sprite_release_types_20261030.h"
void native_main_0206ce54(s32 sprite) {
    s8 child;
    SpriteSlot *slot;
    if (native_data_021c4af4.mainObjects[sprite] != 0) {
        native_fn_0204861c(native_data_021c4af4.slots[sprite].kind,
            ((ReleaseObject *)native_data_021c4af4.mainObjects[sprite])->index);
        native_fn_0202a498(2,native_data_021c4af4.mainObjects[sprite]);
        native_data_021c4af4.mainObjects[sprite] = 0;
    }
    child = native_data_021c4af4.slots[sprite].first;
    if (child < (s8)(child + native_data_021c4af4.slots[sprite].children)) {
        slot = &native_data_021c4af4.slots[sprite];
        do {
            if (native_data_021c4af4.childObjects[child] != 0) {
                native_fn_0204861c(slot->kind,((ReleaseObject *)native_data_021c4af4.childObjects[child])->index);
                native_fn_0202a498(2,native_data_021c4af4.childObjects[child]);
                native_data_021c4af4.childObjects[child] = 0;
            }
            child = (s8)(child+1);
        } while (child < (s8)(slot->first + slot->children));
    }
}
