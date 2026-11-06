typedef unsigned short u16;
typedef unsigned int u32;
typedef struct Event {
    u16 api;
    u16 status;
    u16 reason;
    u16 reserved;
    u16 code;
    u16 pad;
    void *data;
    u16 length;
    u16 index;
} Event;
typedef struct Parameters {
    void *data;
    u16 length;
    u16 mask;
} Parameters;
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
extern int native_fn_ov005_021d7778(Object *, const Event *);
void native_ov005_021d7ab4(Event *event)
{
    Object *object = native_data_021e78c4.object;
    if (!native_fn_ov005_021d7778(object, event))
        return;
    switch (event->reason) {
    case 21:
        {
            Parameters parameters;
            parameters.mask = 1U << event->index;
            parameters.length = event->length;
            parameters.data = event->data;
            if (object->notify)
                object->notify(8, &parameters);
        }
        break;
    case 9:
    case 26:
        {
            u32 mask;
            object->mask &= (u16)~(1U << event->index);
            mask = 1U << event->index;
            if (object->notify)
                object->notify(11, (void *)mask);
        }
        break;
    case 7:
        break;
    }
}
