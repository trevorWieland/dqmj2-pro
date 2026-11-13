/* ov006 row 0x022031A0: 136 bytes.
 *
 * ov006_display_blend_start_022031a0: Starts a display blend/fade on the main or sub BLDCNT register and schedules its completion callback.
 *
 * Evidence: Writes 0x04000050 (main BLDCNT) or 0x04001050 (sub BLDCNT) through 020042E0, sets up callback 02203228 with 0xC8 via 0220490C, and returns early while context byte +9 is busy.
 * Touches: NDS BLDCNT 0x04000050 / 0x04001050; display context 0x0221C180 (+0xC for sub); callback 02203228.
 * Remaining unknowns: The exact fade target and the meaning of the two arguments passed to 020042E0 are not established.
 *
 * The address stays in the symbol and file name because the measurement pairs a
 * compiled symbol to the private ledger row by its eight-hex address; removing
 * it would silently unmatch the row under the pinned private ledger.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220bb48[];
extern void native_fn_020042e0(void);
extern void native_fn_02203228(void);
extern void native_fn_0220490c(void);


asm u32 ov006_display_blend_start_022031a0 (register u32 screen, register u32 arg1, register u32 arg2, register u32 fade)
{
    push {r3, r4, r5, r6, lr}
    sub sp, #0x4
    add r6, r3, #0x0
    ldr r3, =native_data_0220bb48
    add r5, r0, #0x0
    ldrb r4, [r3, #0x8]
    add r0, r1, #0x0
    add r1, r2, #0x0
    add r2, sp, #0x0
    strb r4, [r2, #0]
    ldrb r4, [r3, #0x9]
    cmp r0, #0x1
    strb r4, [r2, #0x1]
    ldrb r4, [r3, #0xa]
    ldrb r3, [r3, #0xb]
    strb r4, [r2, #0x2]
    strb r3, [r2, #0x3]
    bne ov006_022031a0_L2a
    ldr r2, =0x0221c180
    ldr r4, [r2, #0]
    b ov006_022031a0_L30
ov006_022031a0_L2a:
    ldr r2, =0x0221c180
    ldr r4, [r2, #0]
    add r4, #0xc
ov006_022031a0_L30:
    ldrb r2, [r4, #0x9]
    cmp r2, #0x0
    beq ov006_022031a0_L3c
    add sp, #0x4
    mov r0, #0x0
    pop {r3, r4, r5, r6, pc}
ov006_022031a0_L3c:
    cmp r0, #0x1
    add r2, sp, #0x0
    bne ov006_022031a0_L4c
    ldrsb r2, [r2, r5]
    ldr r0, =0x04001050
    blx native_fn_020042e0
    b ov006_022031a0_L54
ov006_022031a0_L4c:
    ldrsb r2, [r2, r5]
    ldr r0, =0x04000050
    blx native_fn_020042e0
ov006_022031a0_L54:
    ldr r1, =native_fn_02203228+1
    mov r0, #0x1
    add r2, r4, #0x0
    mov r3, #0xc8
    bl native_fn_0220490c
    str r0, [r4, #0]
    mov r0, #0x0
    strh r0, [r4, #0x4]
    strb r5, [r4, #0x8]
    strh r6, [r4, #0x6]
    mov r0, #0x1
    strb r0, [r4, #0x9]
    add sp, #0x4
    pop {r3, r4, r5, r6, pc}
    mov r8, r8
}
