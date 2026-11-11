; Minimal boot entry for the flat stub image.
;
; Justified assembly, not decompiled game code: this is the smallest startup that satisfies the
; contract's "linkable boot floor" requirement (docs/platform/contract.md section 2, step 1). It
; mirrors what the matched sources and the boot-register notes imply rather than reproducing the
; game's own startup, which is not recovered:
;   - a stack pointer exists before any C code runs (the ARM9 boot stack is not documented in the
;     public tree, so this uses the top of the stub image's region);
;   - interrupts are masked by setting the CPSR I and F bits, matching the contract's IRQ
;     save/restore row (src/hardware/main/native_main_hw_02007ff4.s sets/restores the same bit);
;   - .data is copied and .bss is zeroed using linker-defined symbols from stub.lcf;
;   - control transfers to main() and never returns (nothing to return to).
; The game's real boot register sequence (IME, POWCNT1, DISPCNT, DISPSTAT, 0x04000580) is the
; unmatched function 0x02026B28 and is deliberately NOT performed here: stubbing hardware behaviour
; is the port's business, and inventing a sequence would misrepresent the reconstruction.
;
; Metrowerks assembler notes: comments start with ';', '#' introduces immediates, and local numeric
; labels are not accepted by mwasmarm, so every label here is named.

    .section .text
    .arm
    .global __startup
    .extern main
    .extern __data_load_start
    .extern __data_start
    .extern __data_end
    .extern __bss_start
    .extern __bss_end
    .type __startup, @function
__startup:
    ; Stack: grow down from inside the image region, 8-byte aligned.
    ldr     sp, =0x021FF000

    ; Mask IRQ and FIQ (CPSR bits 7 and 6), matching the I-bit contract.
    mrs     r0, cpsr
    orr     r0, r0, #0xC0
    msr     cpsr_c, r0

    ; Copy .data from its load address to its run address. For this flat image both are the same
    ; address, so the loop copies zero bytes; it exists so a split load/run layout works unchanged.
    ldr     r0, =__data_load_start
    ldr     r1, =__data_start
    ldr     r2, =__data_end
copy_data:
    cmp     r1, r2
    bhs     zero_bss
    ldr     r3, [r0], #4
    str     r3, [r1], #4
    b       copy_data

    ; Zero .bss.
zero_bss:
    ldr     r1, =__bss_start
    ldr     r2, =__bss_end
    mov     r3, #0
zero_loop:
    cmp     r1, r2
    bhs     run_main
    str     r3, [r1], #4
    b       zero_loop

    ; Run the reconstructed boot loop. main() never returns by construction.
run_main:
    bl      main
hang:
    b       hang
    .size __startup, . - __startup
