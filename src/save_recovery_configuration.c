typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 *descriptor; u8 prefix[0x18]; u32 first; u32 second; u32 bytes; u8 fields28[0x10]; void (*callback)(u32); u32 argument; u8 middle[0xc4]; u32 identity; u32 reserved108; u8 queue[8]; volatile u32 flags; u8 reserved118[8]; u8 scratch[]; } BackupBackend;
extern BackupBackend native_backup_backend;
extern u8 native_backend_validate_tag[];
extern u32 native_backend_initialized;
extern u32 native_backend_identity[];
extern void native_backend_validate(void *);
extern void native_backend_failure(void);
extern u32 native_backend_irq_disable(void);
extern void native_backend_irq_restore(u32);
extern void native_backend_queue_wait(void *);
extern void native_backend_queue_wake(void *);
extern void native_backend_thread_wake(void *);
extern void native_backend_descriptor_select(u32);
extern int save_backend_command(BackupBackend *, u32, int);
u32 save_backend_initialized_get(void) { return native_backend_initialized; }
void save_backend_initialized_check(void) {
    if (!save_backend_initialized_get()) native_backend_failure();
}
void save_backend_initialized_set(u32 value) { native_backend_initialized = value; }
int save_backend_wait(void) {
    BackupBackend *backend = &native_backup_backend;
    u32 interrupt_state = native_backend_irq_disable();
    while (backend->flags & 4) native_backend_queue_wait(backend->queue);
    native_backend_irq_restore(interrupt_state);
    return backend->descriptor[0] == 0;
}
int save_backend_complete(void) { return !(native_backup_backend.flags & 4); }
void save_backend_fifo_callback(u32 channel, u32 value, u32 error) {
    BackupBackend *backend;
    if (channel != 11) return;
    if (!error) return;
    backend = &native_backup_backend;
    value = backend->flags;
    channel = backend->identity;
    backend->flags = value & ~0x20;
    native_backend_thread_wake((void *)channel);
}
int save_backend_configure(u32 type) {
    BackupBackend *backend = &native_backup_backend;
    u32 interrupt_state;
    u32 argument;
    void (*callback)(u32);
    native_backend_validate(native_backend_validate_tag);
    if (!type) native_backend_failure();
    save_backend_initialized_check();
    interrupt_state = native_backend_irq_disable();
    if (backend->flags & 4) {
        do {
            native_backend_queue_wait(backend->queue);
        } while (backend->flags & 4);
    }
    backend->flags |= 4;
    backend->callback = 0;
    backend->argument = 0;
    native_backend_irq_restore(interrupt_state);
    native_backend_descriptor_select(type);
    native_backup_backend.identity = native_backend_identity[1];
    save_backend_command(backend, 2, 1);
    backend->descriptor[3] = 0;
    backend->descriptor[4] = (u32)backend->scratch;
    backend->descriptor[5] = 1;
    save_backend_command(backend, 6, 1);
    callback = backend->callback;
    argument = backend->argument;
    interrupt_state = native_backend_irq_disable();
    backend->flags &= ~0x4c;
    native_backend_queue_wake(backend->queue);
    if (backend->flags & 0x10) native_backend_thread_wake((u8 *)backend + 0x44);
    native_backend_irq_restore(interrupt_state);
    if (callback) callback(argument);
    return backend->descriptor[0] == 0;
}
