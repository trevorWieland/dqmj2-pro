/* ov000 row 0x02212548: 420 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (2 loads, 5 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x19c -> constant 0x02240c74 (image word 0x02240c74)
 *   pool +0x1a0 -> constant 0x0224157c (image word 0x0224157c)
 *   back edge +0x30 -> +0x24
 *   branch +0x48 -> +0x17c
 *   branch +0x5c -> +0x17c
 *   branch +0x6c -> +0x17c
 *   branch +0x94 -> +0x170
 *   branch +0xac -> +0x170
 *   branch +0xb8 -> +0xe0
 *   branch +0x140 -> +0x170
 *   back edge +0x15c -> +0x150
 *   branch +0x16c -> +0x17c
 *   back edge +0x178 -> +0x84
 *   back edge +0x188 -> +0x40
 *   test +0x44 cmp r0, #0
 *   test +0x50 cmp r1, #0
 *   test +0x58 cmpne r1, #0
 *   test +0x68 cmp r7, #0
 *   test +0x90 cmp r1, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xb4 cmp r0, #0
 *   test +0x13c cmp r1, r7
 *   test +0x174 cmp r6, #20
 *   test +0x180 cmp r11, #24
 *   3 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02212548; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_021dfc08(void);
extern void native_fn_02028fac(void);
extern void native_fn_02000ce8(void);
extern void native_fn_02028044(void);
extern void native_fn_0200103c(void);


asm u32 native_ov000_02212548 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #48
    mov r10, r0
    mov r0, #0
    ldr r5, =0x02240c74
    mov r1, r0
    mov r2, r0
    mov r3, r0
    mov r4, #11
ov000_02212548_L24:
    stmia r5!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_02212548_L24
    stmia r5, {r0, r1}
    ldr r9, =0x0224157c
    mov r11, #0
ov000_02212548_L40:
    ldrsh r0, [r9]
    cmp r0, #0
    ble ov000_02212548_L17c
    ldrb r1, [r9, #0x9]
    cmp r1, #0
    ldrne r1, [r9, #0x164]
    cmpne r1, #0
    beq ov000_02212548_L17c
    bl native_fn_021dfc08
    mov r7, r0
    cmp r7, #0
    ble ov000_02212548_L17c
    ldr r0, [r9, #0x74]
    mov r6, #0
    ldr r8, [r0]
    add r4, sp, #0
    add r5, sp, #36
ov000_02212548_L84:
    add r0, r9, r6
    add r0, r0, #256
    ldrsb r1, [r0, #80]
    cmp r1, #0
    blt ov000_02212548_L170
    mov r2, r8
    mov r3, r5
    add r0, r9, #20
    bl native_fn_02028fac
    cmp r0, #0
    beq ov000_02212548_L170
    ldr r0, [r9, #0xa0]
    cmp r0, #0
    beq ov000_02212548_Le0
    mov r0, r4
    bl native_fn_02000ce8
    ldr r1, [r9, #0xa0]
    mov r0, r4
    bl native_fn_02028044
    mov r0, r5
    mov r1, r4
    mov r2, r5
    bl native_fn_0200103c
ov000_02212548_Le0:
    ldr r3, [sp, #0x24]
    ldr r2, [r9, #0x84]
    ldr r1, [sp, #0x28]
    ldr r0, [r9, #0x88]
    add lr, r3, r2
    add r0, r1, r0
    ldr r2, [sp, #0x2c]
    ldr r1, [r9, #0x8c]
    str lr, [sp, #0x24]
    add r12, r2, r1
    str r0, [sp, #0x28]
    str r12, [sp, #0x2c]
    ldr r1, [r10, #0x4]
    ldr r2, [r10]
    sub r3, r1, r0
    smull r1, r0, r3, r3
    sub r3, r2, lr
    ldr r2, [r10, #0x8]
    smlal r1, r0, r3, r3
    sub r2, r2, r12
    smlal r1, r0, r2, r2
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    cmp r1, r7
    bge ov000_02212548_L170
    ldr r5, =0x02240c74
    mov r6, r9
    mov r4, #22
ov000_02212548_L150:
    ldmia r6!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_02212548_L150
    ldmia r6, {r0, r1}
    stmia r5, {r0, r1}
    mov r11, #24
    b ov000_02212548_L17c
ov000_02212548_L170:
    add r6, r6, #1
    cmp r6, #20
    blt ov000_02212548_L84
ov000_02212548_L17c:
    add r11, r11, #1
    cmp r11, #24
    add r9, r9, #360
    blt ov000_02212548_L40
    ldr r0, =0x02240c74
    ldrsh r0, [r0]
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
