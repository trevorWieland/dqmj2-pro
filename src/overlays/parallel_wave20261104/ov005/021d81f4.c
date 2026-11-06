typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct Event {
    u16 api;
    u16 status;
    u16 reason;
    u16 reserved[2];
    u16 selector;
} Event;
typedef struct Configuration {
    u8 pad[0x16];
    u16 flag;
} Configuration;
typedef struct Object {
    u8 pad[0x50e4];
    u16 selector;
    u16 mask;
    u16 first;
    u16 second;
    u32 active;
    u32 state;
    u32 phase;
    int (*notify)(int, void *);
    Configuration *configuration;
    u8 pad2[0x20];
    u8 descriptor[0xc0];
    u8 pad3[0x444];
    u8 saved[24];
} Object;
typedef struct Globals {
    u32 reserved;
    Object *object;
} Globals;
extern Globals native_data_021e78c4;
extern int native_fn_ov005_021d7778(Object *, const Event *);
extern void native_fn_02008e0c(const void *, void *, u32);
extern void native_fn_ov005_021d812c(void *);
extern int native_fn_02012cb8(void (*)(void *), void *, void *, int, int);
extern void native_fn_ov005_021d773c(Object *, int, int);
extern int native_fn_02013080(void (*)(Event *), void *, u16, void *, u16, u16);
extern void native_fn_ov005_021d7874(Object *, int, Event *);
void native_ov005_021d81f4(Event *event)
{
    Object *object = native_data_021e78c4.object;
    if (event && !native_fn_ov005_021d7778(object, event))
        return;
    if (!event) {
        u16 saved[3];
        native_fn_02008e0c(object->descriptor + 12, saved, 6);
        if (object->notify)
            object->notify(9, object->descriptor);
        native_fn_02008e0c(object->descriptor + 20, object->saved, 24);
        native_fn_02008e0c(saved, object->descriptor + 12, 6);
        object->state = 1;
        native_fn_ov005_021d773c(object, 12,
            native_fn_02012cb8(native_fn_ov005_021d812c, object->descriptor, object->saved, 1, 0));
        return;
    }
    if (event->api == 12) {
        object->selector = event->selector;
        native_fn_ov005_021d773c(object, 14,
            native_fn_02013080(native_ov005_021d81f4, (u8 *)object + 0x1120,
                object->second, (u8 *)object + 0xf00, object->first,
                (u16)(object->configuration->flag == 0)));
        return;
    }
    if (event->api != 14)
        return;
    switch (event->reason) {
    case 10:
        native_fn_ov005_021d7874(object, 5, event);
        break;
    }
}
