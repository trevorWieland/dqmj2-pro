typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 *descriptor; u8 prefix[0x18]; u32 first; u32 second; u32 bytes; u32 reserved28; u32 operation; u32 mode; u32 final; u32 callback; u32 argument; u8 middle[0xc4]; u32 identity; u32 reserved108; u8 queue[8]; u32 flags; } BackupBackend;
extern BackupBackend native_backup_backend;
extern u32 native_backup_identity_source[];
extern u8 native_backend_validate_tag[];
extern void native_backend_validate(void *);
extern u32 native_backend_irq_disable(void);
extern void native_backend_irq_restore(u32);
extern void native_backend_queue_wait(void *);
extern void native_backend_schedule(void (*)(BackupBackend *));
extern void native_backend_execute(BackupBackend *);
extern void native_fn_ov006_022053b8(u16, u32);
extern void native_backup_bus_unlock(u16, u32);
extern int native_backend_poll_complete(void);
extern void native_backend_wait_idle(void);
int save_backend_transfer(u32 first, u32 second, u32 bytes, u32 callback, u32 argument, u32 asynchronous, u32 operation, u32 mode, u32 final) {
    BackupBackend *backend = &native_backup_backend;
    u32 interrupt_state;
    native_backend_validate(native_backend_validate_tag);
    interrupt_state = native_backend_irq_disable();
    while (backend->flags & 4) native_backend_queue_wait(backend->queue);
    backend->flags |= 4;
    backend->callback = callback;
    backend->argument = argument;
    native_backend_irq_restore(interrupt_state);
    backend->first = first;
    backend->second = second;
    backend->bytes = bytes;
    backend->operation = operation;
    backend->mode = mode;
    backend->final = final;
    if (asynchronous) {
        native_backend_schedule(native_backend_execute);
        return 1;
    }
    native_backup_backend.identity = native_backup_identity_source[1];
    native_backend_execute(backend);
    return backend->descriptor[0] == 0;
}
int save_backend_busy(void) { return native_backup_backend.flags != 0; }
u32 save_backend_result(void) { return native_backup_backend.descriptor[0]; }
u32 save_backend_capacity(void) { return native_backup_backend.descriptor[6]; }
u32 save_backend_page_alternate(void) { return native_backup_backend.descriptor[7]; }
u32 save_backend_page_size(void) { return native_backup_backend.descriptor[9]; }
int save_backend_completed(void) { return native_backend_poll_complete(); }
void save_backend_wait_completed(void) { native_backend_wait_idle(); }
void native_ov006_022054a0(u16 identifier) { native_fn_ov006_022053b8(identifier, 2); }
void save_backend_unlock(u16 identifier) {
    if (!save_backend_completed()) save_backend_wait_completed();
    native_backup_bus_unlock(identifier, 2);
}
