typedef unsigned short u16;
typedef signed short s16;
typedef unsigned int u32;
typedef struct VAlarmNodeView VAlarmNodeView;
struct VAlarmNodeView {
    u32 handler;
    u32 argument;
    u32 tag;
    u32 frame;
    s16 scan;
    u16 padding;
    VAlarmNodeView *previous;
    VAlarmNodeView *next;
};
typedef struct { u32 words[3]; VAlarmNodeView *head; VAlarmNodeView *tail; } VAlarmQueueView;
extern VAlarmQueueView native_host_arm7_valarm_queue_038078b4;
extern void native_host_arm7_arm_037fd9b8(VAlarmNodeView *);
void native_host_arm7_arm_037fd7a8(VAlarmNodeView *entry) {
    VAlarmNodeView *next = native_host_arm7_valarm_queue_038078b4.head;
    while (next != (void *)0) {
        if (next->frame >= entry->frame) {
            if (next->frame != entry->frame || next->scan > entry->scan) {
                VAlarmNodeView *previous = next->previous;
                entry->previous = previous;
                entry->next = next;
                next->previous = entry;
                if (previous != (void *)0) {
                    previous->next = entry;
                } else {
                    native_host_arm7_valarm_queue_038078b4.head = entry;
                    native_host_arm7_arm_037fd9b8(entry);
                }
                return;
            }
        }
        next = next->next;
    }
    VAlarmNodeView *previous = native_host_arm7_valarm_queue_038078b4.tail;
    entry->previous = previous;
    entry->next = (void *)0;
    native_host_arm7_valarm_queue_038078b4.tail = entry;
    if (previous != (void *)0) {
        previous->next = entry;
    } else {
        native_host_arm7_valarm_queue_038078b4.head = entry;
        native_host_arm7_arm_037fd9b8(entry);
    }
}
