typedef unsigned int u32;
typedef struct Node Node;
struct Node {
    Node *next;
};

extern Node *native_data_020e3780;
extern u32 native_fn_02007ff4(void);
extern u32 native_fn_02008008(u32);

u32 native_main_02009a5c(void) {
    u32 interrupt = native_fn_02007ff4();
    u32 count = 0;
    Node *cursor = native_data_020e3780;
    if (cursor) {
        do {
            cursor = cursor->next;
            count++;
        } while (cursor);
    }
    native_fn_02008008(interrupt);
    return count;
}
