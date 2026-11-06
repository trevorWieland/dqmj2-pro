typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u32 *descriptor; u32 command; u8 middle[0x10c]; volatile u32 flags; } BackupBackend;
extern int native_fifo_ready(u32, u32);
extern int native_fifo_send(u32, u32, u32);
extern void native_backend_pause(u32);
extern void native_cache_clean(void *, u32);
extern void native_cache_drain(void);
extern void native_cache_invalidate(void *, u32);
extern u32 native_backend_irq_disable(void);
extern void native_backend_irq_restore(u32);
extern void native_backend_queue_wait(void *);
int save_backend_command(BackupBackend *backend, u32 operation, int attempts) {
    u32 interrupt_state;
    u32 status;
    if (!(backend->flags & 2)) {
        backend->flags |= 2;
        if (!native_fifo_ready(11, 1)) {
            do {
                native_backend_pause(100);
            } while (!native_fifo_ready(11, 1));
        }
        save_backend_command(backend, 0, 1);
    }
    native_cache_clean(backend->descriptor, 0x60);
    native_cache_drain();
    do {
        backend->command = operation;
        backend->flags |= 0x20;
        while (native_fifo_send(11, operation, 1) < 0) {}
        if (!operation) {
            u32 descriptor = (u32)backend->descriptor;
            while (native_fifo_send(11, descriptor, 1) < 0) {}
        }
        interrupt_state = native_backend_irq_disable();
        while (backend->flags & 0x20) native_backend_queue_wait(0);
        native_backend_irq_restore(interrupt_state);
        native_cache_invalidate(backend->descriptor, 0x60);
        status = backend->descriptor[0];
        if (status != 4) break;
        --attempts;
    } while (attempts > 0);
    return status == 0;
}
