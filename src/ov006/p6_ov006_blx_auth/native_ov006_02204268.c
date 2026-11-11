#include "context.h"

/* One node of the ov006 global doubly-linked list. The list head is itself a
   node: head->prev is the tail, head->next is the first element. */
struct native_list_node {
    struct native_list_node *prev;
    struct native_list_node *next;
};

/* Interrupt-guard pair: the first call returns the key that the second call
   releases with. Both are ARM code in main, called from Thumb through BLX. */
extern s32 native_fn_02005d50(s32 lock);
extern void native_fn_02005d20(s32 key);

/* ov006 row 0x02204268: 34 bytes. Remove a node from the global list: relink
   the neighbours, clear the node's own links, all under the shared lock. Both
   calls at +0x02 and +0x1C target ARM code and are BLX immediates in the image
   (01 F6 70 ED / 01 F6 4C ED). Unknown: the lock identity (1) and the callee
   names; the returned key is inferred from r0 being carried from the first call
   into the second. */
void native_ov006_02204268(struct native_list_node *node)
{
    s32 key = native_fn_02005d50(1);

    node->prev->next = node->next;
    node->next->prev = node->prev;
    node->next = 0;
    node->prev = 0;
    native_fn_02005d20(key);
}
