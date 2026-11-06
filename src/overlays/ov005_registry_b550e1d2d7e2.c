typedef unsigned int u32;
typedef struct Node {u32 words[10];struct Node *next;} Node;
extern Node *data_ov005_021e78c0;
extern int func_02019da8(const char *,const char *);

void native_ov005_021d7338(Node *node) {
    Node *current=data_ov005_021e78c0;
    if(!current){data_ov005_021e78c0=node;node->next=0;return;}
    while(1){Node *next;if(current==node)return;next=current->next;if(!next){current->next=node;node->next=0;return;}current=next;}
}

Node *native_ov005_021d738c(const char *name) {
    Node *current=data_ov005_021e78c0;
    while(current){if(!func_02019da8(name,(const char *)current->words[0]))break;current=current->next;}
    return current;
}
