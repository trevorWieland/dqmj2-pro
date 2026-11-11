#ifndef J2P_PLATFORM_H
#define J2P_PLATFORM_H

/*
 * Platform contract for the DQM Joker 2 Professional recompilation/port.
 *
 * This header is an interface description, not a build target. Every group
 * below is derived from matched source; each declaration names the matched
 * file/function that established the shape, or is marked INFERRED when the
 * shape was read from disassembly of an unmatched function. UNKNOWN entries
 * have no matched reader and must not be implemented by guessing.
 *
 * Addresses are Nintendo DS ARM9 bus addresses. Registers are volatile u16/u32
 * as noted. The host must provide these symbols (or equivalent shims) before
 * the reconstructed game code can link and boot.
 */

#include <stdint.h>

typedef uint8_t u8;
typedef int8_t s8;
typedef uint16_t u16;
typedef int16_t s16;
typedef uint32_t u32;
typedef int32_t s32;

/* ------------------------------------------------------------------------- */
/* Interrupt control                                                          */
/* ------------------------------------------------------------------------- */
/* Evidence: src/itcm/restart.c (native_itcm_01ff81b4) writes IME = 0 before
 * restoring context; src/runtime/20261101_fifo_send136/native_main_0200a440.c
 * brackets the FIFO write with native_fn_02007ff4/native_fn_02008008. The
 * register pair 0x04000208 (IME) + 0x04000210/0x04000214 is the DS interrupt
 * master/enable/ack block; a port must model a maskable IRQ source. */
u32 j2p_irq_save(void);      /* native_fn_02007ff4: returns prior IME state */
void j2p_irq_restore(u32 state); /* native_fn_02008008 */

/* Evidence: src/hardware/bootstrap_bios/native_main_bios_020002ae.s is the
 * matched-symbol `IntrWait`, 0x020003e6 is `VBlankIntrWait`. Ports must be able
 * to block until the vertical-blank IRQ, or run a virtual clock that does. */
void j2p_intr_wait(u32 discard, u32 mask);
void j2p_vblank_intr_wait(u32 discard, u32 state);

/* ------------------------------------------------------------------------- */
/* Boot / clocks / display                                                   */
/* ------------------------------------------------------------------------- */
/* Evidence: src/main/p1e_main_02026b28/native_main_02026b28.c is the matched
 * early-boot routine. It calls the clock/IRQ bring-up, then writes:
 *   0x04000208 (IME) = 1
 *   0x04000304 (POWCNT1) with mask 0xfffffdf1 | 0xe | 0x200
 *   0x04000050 (DISPCNT) = 0
 *   0x04000060 (DISPSTAT) read-modify-write x4
 *   0x04000580 (u32) = 0xbfff0000
 * then calls the graphics, sound and runtime init subsystems in a fixed order.
 * A port must provide these registers as memory or traps; the exact W1C vs RW
 * semantics of DISPSTAT are a hardware assumption (INFERRED from the DS map). */
void j2p_boot_sequence(void); /* mirrors native_main_02026b28 */

/* Evidence: src/runtime/runtime03/native_main_02041774.c calls
 * native_fn_020042e0(0x04000050, mode_word, flag) and the same for
 * 0x04001050 (engine B). native_fn_020042e0 is UNKNOWN by name; the inference
 * is a display mode/control setter (argument order: register address, mode
 * word, byte flag). */
void j2p_display_control(u32 register_address, u32 mode_word, u32 flag);

/* ------------------------------------------------------------------------- */
/* Memory / heap                                                             */
/* ------------------------------------------------------------------------- */
/* Evidence: src/ov006/p1k_ov006_thumb/native_main_021f1f0c.c allocates
 * `count * size` through a vtable slot at 0x0221aad0 + 0x04 and zero-fills the
 * result. src/main_sdk_aux/20261101_frame_heap_*/ and 20261101_heap_*/
 * reconstruct the original two-level heap (arena, attribute, search). A port
 * may map these onto a host allocator, but must preserve the "returns 0 on
 * failure" contract and the 0x18-byte block header sizes seen there. */
void *j2p_mem_alloc(u32 bytes); /* vtable +0x04; 0 on failure */
void j2p_mem_free(void *block); /* vtable +0x0c is a flush; free path INFERRED */

/* Evidence: named SDK symbols 0x0200064a `CpuSet` and 0x020007a6 `CpuFastSet`
 * are present in main; matched callers exist through native_fn_0200064a /
 * native_fn_020007a6. Both take (source, destination, control) with the DS
 * fill/copy bit in the control word. */
void j2p_cpu_set(const void *source, void *destination, u32 control);
void j2p_cpu_fast_set(const void *source, void *destination, u32 control);

/* ------------------------------------------------------------------------- */
/* DMA                                                                       */
/* ------------------------------------------------------------------------- */
/* Evidence: src/itcm/dma.c (native_itcm_01ff8448 / 8488 / 84f8 / 851c).
 * Registers are 0x040000b0 + channel*12: SAD, DAD, CNT. The matched code reads
 * the channel 0 SAD twice as a write barrier and writes 0x81400001 as a
 * control word for the immediate-copy form. A port must implement at least a
 * synchronous copy; async completion is INFERRED. */
void j2p_dma_start(s32 channel, u32 source, u32 destination, u32 control);
void j2p_dma_wait(s32 channel);

/* ------------------------------------------------------------------------- */
/* ARM7 link (IPC FIFO)                                                      */
/* ------------------------------------------------------------------------- */
/* Evidence: src/runtime/20261101_fifo_send136/native_main_0200a440.c.
 * Word layout: bitfield channel:5, flag:1, payload:26. Status register
 * 0x04000184: bit 14 = FIFO full (returns -1), bit 1 = send-empty (returns
 * -2); data register 0x04000188 receives the 32-bit word. A port must provide
 * a bidirectional FIFO to the ARM7 image or a stub that never reports full. */
s32 j2p_fifo_send(u32 channel, u32 payload, u32 flag); /* 0 ok, -1 full, -2 empty */

/* Evidence: the ARM7 side is reconstructed separately under src/arm7/ (e.g.
 * src/arm7/20261030_bulk_host02/native_arm7_wram_037fee58.c) and the utility
 * ARM7 image under ports-level sources. The ARM7 boot handshake itself is
 * UNKNOWN on the ARM9 side: no matched ARM9 reader of the boot flags exists in
 * src/ yet. */
void j2p_arm7_sync(void); /* UNKNOWN: no matched ARM9 caller */

/* ------------------------------------------------------------------------- */
/* Card / file system                                                        */
/* ------------------------------------------------------------------------- */
/* Evidence: src/mechanics_save/20261029_card_command.c writes the card bus
 * command register block at 0x040001a1 (control byte 0xc0 + 8 command bytes)
 * and polls 0x040001a4 bit 31 for busy. This is the raw card command layer, not
 * the NitroFS file API. The file API used by matched code is UNKNOWN: no
 * matched reader calls a named FS_* entry; the host port models the same bus
 * through ports/native-storage and ports/runtime/card_reader64. */
void j2p_card_command(u32 first, u32 second);
void j2p_card_wait_busy(void);

/* ------------------------------------------------------------------------- */
/* Sound                                                                     */
/* ------------------------------------------------------------------------- */
/* Evidence: sound registers 0x04000400-0x040005ff appear only in ARM7/utility
 * sources under src/arm7/ and src/utility/ in this checkout, not in matched
 * main-module code. The main game's sound API is UNKNOWN: it presumably crosses
 * the FIFO (j2p_fifo_send) to the ARM7 sound driver, but no matched main-side
 * caller has been identified. Do not implement a guess. */
void j2p_sound_init(void); /* UNKNOWN */

/* ------------------------------------------------------------------------- */
/* Input                                                                     */
/* ------------------------------------------------------------------------- */
/* Evidence: no matched main-module source reads KEYINPUT (0x04000130) or the
 * key interrupt block; the only input handling in the tree is host-side
 * (ports/native-host maps window input into a 256x192 viewport). The guest
 * input service is UNKNOWN and must be recovered from the ARM9 touch/key
 * reader before a port can be input-complete. */
u32 j2p_input_read(void); /* UNKNOWN */

/* ------------------------------------------------------------------------- */
/* Threads / locks                                                           */
/* ------------------------------------------------------------------------- */
/* Evidence: src/main_sdk_aux/20261101_lock_pair (native_main_02005f08) and
 * 20261101_thread_remove124 reconstruct the SDK lock/thread primitives; the
 * matched shapes acquire/release a pointer-sized lock word. A port may map
 * them to a single-threaded no-op only if it never concurrently runs guest
 * threads. */
void j2p_lock_acquire(void *lock);
void j2p_lock_release(void *lock);

#endif /* J2P_PLATFORM_H */
