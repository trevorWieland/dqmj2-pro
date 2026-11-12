/* main row 0x0209b368: 208 bytes.
 *
 * What it does: Moves 2-register chunks between two pointers with writeback block moves (2 loads, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0xb8 -> native_data7_021d19c8 (image word 0x021d19c8)
 *   pool +0xbc -> constant 0x00ffffff (image word 0x00ffffff)
 *   pool +0xc0 -> native_data4_021d19c8 (image word 0x021d19c8)
 *   pool +0xc4 -> constant 0x6c078965 (image word 0x6c078965)
 *   pool +0xc8 -> constant 0x5d588b65 (image word 0x5d588b65)
 *   pool +0xcc -> constant 0x00269ec3 (image word 0x00269ec3)
 *   branch +0x16 -> +0x86
 *   branch +0x28 -> +0x86
 *   branch +0x3a -> +0x86
 *   branch +0xa2 -> +0xb2
 *   test +0xa0 cmp r4, #0x0
 *   3 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0209b368; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 208 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data7_021d19c8[];
extern void native_fn_020081fc(void);
extern void native_fn_02007a9c(void);
extern u8 native_data4_021d19c8[];
extern void native_fn_02026124(void);


asm u32 native_main_0209b368 (register u32 a0)
{
    push {r4, r5, r6, lr}
    sub sp, #0x8
    add r4, r0, #0x0
    ldr r0, =native_data7_021d19c8
    mov r1, #0x0
    ldr r2, [r0, #0x4]
    ldr r3, [r0, #0]
    mov r0, #0x0
    eor r1, r2
    eor r0, r3
    orr r0, r1
    bne main_0209b368_L86
    ldr r0, =native_data7_021d19c8
    mov r1, #0x0
    ldr r2, [r0, #0xc]
    ldr r3, [r0, #0x8]
    mov r0, #0x0
    eor r1, r2
    eor r0, r3
    orr r0, r1
    bne main_0209b368_L86
    ldr r0, =native_data7_021d19c8
    mov r1, #0x0
    ldr r2, [r0, #0x14]
    ldr r3, [r0, #0x10]
    mov r0, #0x0
    eor r1, r2
    eor r0, r3
    orr r0, r1
    bne main_0209b368_L86
    add r0, sp, #0x0
    blx native_fn_020081fc
    blx native_fn_02007a9c
    add r5, r1, #0x0
    ldr r1, [sp]
    ldr r2, [sp, #0x4]
    add r3, r0, #0x0
    lsl r0, r2, #0x8
    lsr r1, r1, #0x18
    orr r1, r0
    ldr r6, =0x00ffffff
    lsr r2, r2, #0x18
    mov r0, #0x0
    and r1, r6
    lsr r6, r3, #0x8
    lsl r5, r5, #0x18
    lsl r3, r3, #0x18
    orr r1, r3
    str r1, [sp]
    and r2, r0
    orr r5, r6
    orr r2, r5
    add r1, sp, #0x0
    str r2, [sp, #0x4]
    ldmia r1!, {r2, r3}
    ldr r1, =native_data4_021d19c8
    stmia r1!, {r2, r3}
    ldr r3, =0x6c078965
    ldr r1, =native_data7_021d19c8
    ldr r2, =0x5d588b65
    str r3, [r1, #0x8]
    str r2, [r1, #0xc]
    ldr r2, =0x00269ec3
    str r2, [r1, #0x10]
    str r0, [r1, #0x14]
main_0209b368_L86:
    ldr r3, =native_data7_021d19c8
    ldr r0, [r3, #0x8]
    ldr r1, [r3, #0xc]
    ldmia r3!, {r2, r3}
    blx native_fn_02026124
    ldr r2, =native_data7_021d19c8
    ldr r3, [r2, #0x10]
    ldr r5, [r2, #0x14]
    add r0, r3, r0
    adc r5, r1
    str r0, [r2, #0]
    str r5, [r2, #0x4]
    cmp r4, #0x0
    beq main_0209b368_Lb2
    mov r1, #0x0
    add r0, r5, #0x0
    mov r3, #0x0
    add r2, r4, #0x0
    blx native_fn_02026124
    add r5, r1, #0x0
main_0209b368_Lb2:
    add r0, r5, #0x0
    add sp, #0x8
    pop {r4, r5, r6, pc}
}
