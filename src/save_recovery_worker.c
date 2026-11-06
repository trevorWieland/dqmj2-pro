typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 *descriptor; u8 prefix[0x18]; u32 first; u32 second; u32 bytes; u32 reserved28; u32 operation; u32 mode; u32 final; u32 callback; u32 argument; u8 middle[0xc4]; u32 identity; u32 reserved108; u8 queue[8]; volatile u32 flags; u8 reserved118[8]; u8 scratch[]; } BackupBackend;
extern BackupBackend native_backup_backend;
extern u8 native_backend_validate_tag[];
extern void native_backend_validate(void *);
extern u32 save_backend_page_alternate(void);
extern void native_cache_invalidate(void *, u32);
extern void native_cache_clean(void *, u32);
extern void native_cache_drain(void);
extern void native_copy(const void *, void *, u32);
extern int native_backend_command(BackupBackend *, u32, u32);
extern u32 native_backend_irq_disable(void);
extern void native_backend_irq_restore(u32);
extern void native_backend_queue_wake(void *);
extern void native_backend_thread_wake(void *);
void save_backend_worker(BackupBackend *backend) {
    u32 final;
    u32 maximum;
    u8 *scratch;
    u32 operation;
    u32 mode;
    u32 interrupt_state;
    u32 argument;
    void (*callback)(u32);
    operation = backend->operation;
    final = backend->final;
    mode = backend->mode;
    maximum = 0x100;
    native_backend_validate(native_backend_validate_tag);
    if (operation == 11) maximum = save_backend_page_alternate();
    else if (operation == 15) maximum = native_backup_backend.descriptor[8];
    scratch = backend->scratch;
    do {
        u32 count = backend->bytes;
        if (maximum < count) count = maximum;
        backend->descriptor[5] = count;
        if (backend->flags & 0x40) {
            backend->flags &= ~0x40;
            backend->descriptor[0] = 7;
            break;
        }
        switch (final) {
        case 0:
            native_cache_invalidate(scratch, count);
            backend->descriptor[3] = backend->first;
            backend->descriptor[4] = (u32)scratch;
            break;
        case 1:
        case 2:
            native_copy((void *)backend->first, scratch, count);
            native_cache_clean(scratch, count);
            native_cache_drain();
            backend->descriptor[3] = (u32)scratch;
            backend->descriptor[4] = backend->second;
            break;
        case 3:
            backend->descriptor[3] = backend->first;
            backend->descriptor[4] = backend->second;
            break;
        default:
            break;
        }
        if (!native_backend_command(backend, operation, mode)) break;
        if (final == 2) {
            switch (native_backend_command(backend, 9, 1)) {
            case 0:
                goto completed;
            default:
                break;
            }
        } else if (final == 0) native_copy(scratch, (void *)backend->second, count);
        backend->first += count;
        backend->second += count;
        backend->bytes -= count;
    } while (backend->bytes);
completed:
    callback = (void (*)(u32))backend->callback;
    argument = backend->argument;
    interrupt_state = native_backend_irq_disable();
    backend->flags &= ~0x4c;
    native_backend_queue_wake(backend->queue);
    if (backend->flags & 0x10) native_backend_thread_wake((u8 *)backend + 0x44);
    native_backend_irq_restore(interrupt_state);
    if (!callback) return;
    callback(argument);
}
