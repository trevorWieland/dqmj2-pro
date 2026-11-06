#include "native_range_types.h"
extern u32 native_fn_02036830(const Node *, u32);
u32 native_main_0203694c(const Map *const *holder, u32 key) {
    const Node *node = (*holder)->head;
    while (node) {
        if (node->first <= key && key <= node->last) return native_fn_02036830(node, key);
        node = node->next;
    }
    return 65535;
}
