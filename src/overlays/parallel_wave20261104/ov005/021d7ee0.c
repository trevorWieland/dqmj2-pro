typedef unsigned short u16;
typedef struct Event {
    u16 api;
    u16 status;
    u16 reason;
    u16 reserved;
    u16 code;
    u16 pad[3];
    u16 index;
    u16 other;
} Event;
typedef struct Object {
    unsigned char pad[0x50e4];
    u16 selector;
    u16 mask;
    unsigned int reserved[4];
    void (*notify)(int, void *);
    void *configuration;
} Object;
typedef struct Globals {
    unsigned int reserved;
    Object *object;
} Globals;
extern Globals native_data_021e78c4;
extern void native_fn_ov005_021d7fcc(Event *);
extern void native_fn_ov005_021d77ac(Object *);
void native_ov005_021d7ee0(Event *event)
{
    Object *object = native_data_021e78c4.object;
    if (event->code == 0) {
        native_fn_ov005_021d7fcc(event);
        return;
    }
    if (event->status)
        return;
    switch (event->code) {
    case 7:
        {
            int empty = object->mask == 0;
            object->mask |= (u16)(1 << event->index);
            if (object->notify)
                object->notify(10, event);
            if (empty)
                native_fn_ov005_021d77ac(object);
        }
        break;
    case 2:
        {
            void *configuration = object->configuration;
            if (object->notify)
                object->notify(5, configuration);
        }
        break;
    case 0:
    case 9:
    case 26:
        break;
    }
}
