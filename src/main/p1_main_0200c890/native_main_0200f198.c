#include "context.h"

typedef struct Node {
    u32 pad0;
    u32 pad4;
    struct Node *next;  /* +0x08 */
} Node;

extern u32 native_fn_02007ff4(void);
extern void native_fn_02008008(u32 state);

/* Remove `node` from the singly linked list reached through `head`.  The list
   is walked with interrupts masked; a node that is not present is ignored. */
void native_main_0200f198(Node **head, Node *node)
{
    Node *current;
    Node *previous;
    u32 irq;

    if (head == 0)
        return;
    irq = native_fn_02007ff4();
    current = *head;
    previous = current;
    if (current != 0) {
        do {
            if (current == node) {
                Node *next = current->next;
                if (current == previous)
                    *head = next;
                else
                    previous->next = next;
                break;
            }
            previous = current;
            current = current->next;
        } while (current != 0);
    }
    native_fn_02008008(irq);
}
