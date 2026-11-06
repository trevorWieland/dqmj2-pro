typedef unsigned int u32;
typedef struct QueueNode QueueNode;
struct QueueNode { u32 opaque[5]; QueueNode *previous; QueueNode *next; };
typedef struct QueueView { u32 opaque[3]; QueueNode *head; QueueNode *tail; } QueueView;
typedef char node_size[(sizeof(QueueNode)==28)?1:-1];
typedef char queue_prefix_size[(sizeof(QueueView)==20)?1:-1];
extern QueueView native_host_arm7_data_038078b4;
void native_arm7_wram_037fd84c(QueueNode *node) {
    QueueNode *previous;
    QueueNode *next;
    if (node == 0) return;
    next = node->next;
    previous = node->previous;
    if (next) next->previous = previous;
    else native_host_arm7_data_038078b4.tail = previous;
    if (previous) previous->next = next;
    else native_host_arm7_data_038078b4.head = next;
}
