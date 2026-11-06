typedef unsigned char u8;
typedef unsigned int u32;

typedef struct {
    u8 prefix[0x33];
    u8 marker;
} SavedMarkerRecord;

extern SavedMarkerRecord *native_record_by_id(u32 id);
extern void *native_record_display_context(void);
extern void native_record_display(void *context, int mode, int argument, int marker, int reserved, u8 choice);

void saved_record33_display(u32 id, int argument) {
    u8 marker = native_record_by_id(id)->marker;
    int choice;
    if (marker)
        choice = 18;
    else
        choice = 12;
    native_record_display(native_record_display_context(), 1, argument, marker, 0, (u8)choice);
}
