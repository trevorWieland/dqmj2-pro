#include "context.h"

/* Same global doubly-linked list as native_ov006_02204268: the head node's
   prev pointer is the tail, and every node keeps prev at +0 and next at +4. */
struct native_list_node {
    struct native_list_node *prev;
    struct native_list_node *next;
};

extern s32 native_fn_02005d50(s32 lock);
extern void native_fn_02005d20(s32 key);

/* ov006 row 0x0220428C: 30 bytes. Append a node at the tail of the global list
   under the shared lock: the tail's next becomes the new node, the new node
   points back at the tail and forward at the head sentinel, and the head's prev
   becomes the new node. Both calls at +0x08 and +0x1E target ARM code and are
   BLX immediates in the image (01 F6 5C ED / 01 F6 3C ED). Unknown: the lock
   identity (1) and the callee names; the returned key is inferred from r0 being
   carried from the first call into the second. */
void native_ov006_0220428c(struct native_list_node *head, struct native_list_node *node)
{
    s32 key = native_fn_02005d50(1);

    head->prev->next = node;
    node->prev = head->prev;
    node->next = head;
    head->prev = node;
    native_fn_02005d20(key);
}
