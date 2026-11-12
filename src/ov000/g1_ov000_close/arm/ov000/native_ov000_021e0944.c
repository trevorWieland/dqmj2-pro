/* ov000 row 0x021e0944: 540 bytes.
 *
 * What it does: 128 instructions; 23 call(s) to 0x0205be64, 0x0205be4c, 0x0205be88, +20 more; loops (back edge at +0x0c); returns through pop {r3, r4, r5, r6, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x200 -> constant 0x02232344 (image word 0x02232344)
 *   pool +0x204 -> constant 0x0223244c (image word 0x0223244c)
 *   pool +0x208 -> constant 0x02232458 (image word 0x02232458)
 *   pool +0x20c -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x210 -> constant 0x022324e4 (image word 0x022324e4)
 *   pool +0x214 -> constant 0x0223238c (image word 0x0223238c)
 *   pool +0x218 -> constant 0x022323e4 (image word 0x022323e4)
 *   branch +0x1c -> +0x78
 *   branch +0x74 -> +0x150
 *   branch +0x80 -> +0x90
 *   branch +0x8c -> +0x150
 *   branch +0xc4 -> +0x150
 *   branch +0xd0 -> +0x104
 *   branch +0x100 -> +0x150
 *   branch +0x108 -> +0x138
 *   branch +0x134 -> +0x150
 *   branch +0x170 -> +0x1e8
 *   branch +0x17c -> +0x1e8
 *   branch +0x198 -> +0x1c4
 *   test +0x18 cmp r4, r0
 *   test +0x7c cmp r4, r0
 *   test +0x94 cmp r0, #2
 *   test +0xc0 cmp r0, #0
 *   test +0xc8 cmp r6, #0
 *   test +0xd4 cmp r5, #1
 *   test +0x104 cmp r6, #1
 *   test +0x168 cmp r0, #1
 *   test +0x16c cmpeq r4, #6
 *   test +0x174 cmp r0, #1
 *   test +0x178 cmpeq r4, #5
 *   test +0x194 cmp r0, #0
 *   4 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e0944; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0205be64(void);
extern void native_fn_0205be4c(void);
extern void native_fn_0205be88(void);
extern void native_fn_0205c378(void);
extern void native_fn_0205c3a8(void);
extern void native_fn_0205beb4(void);
extern void native_fn_02029870(void);
extern void native_fn_0205bee4(void);
extern void native_fn_021d84e8(void);
extern void native_fn_0205c020(void);
extern void native_fn_0205bf3c(void);
extern void native_fn_021e4744(void);
extern void native_fn_021e0898(void);
extern void native_fn_0205c030(void);
extern void native_fn_021da5e4(void);
extern void native_fn_021dbbb8(void);
extern void native_fn_021dae04(void);


asm u32 native_ov000_021e0944 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #44
    mov r6, r0
    bl native_fn_0205be64
    mov r4, r0
    mvn r0, #0
    cmp r4, r0
    bne ov000_021e0944_L78
    mov r0, #0
    bl native_fn_0205be4c
    ldr r0, =0x02232344
    bl native_fn_0205be88
    ldr r0, =0x0223244c
    bl native_fn_0205c378
    ldr r0, =0x02232458
    bl native_fn_0205c3a8
    mov r0, #0
    str r0, [sp, #0x8]
    bl native_fn_0205beb4
    str r0, [sp, #0xc]
    mov r2, #0
    ldr r0, =0x022322d4
    add r1, sp, #8
    str r2, [sp, #0x10]
    bl native_fn_02029870
    mov r0, #0
    bl native_fn_0205bee4
    mov r1, #1
    bl native_fn_021d84e8
    b ov000_021e0944_L150
ov000_021e0944_L78:
    sub r0, r0, #1
    cmp r4, r0
    bne ov000_021e0944_L90
    mov r0, #2
    bl native_fn_0205c020
    b ov000_021e0944_L150
ov000_021e0944_L90:
    bl native_fn_0205bf3c
    cmp r0, #2
    movne r0, #1
    moveq r0, #0
    and r5, r0, #255
    add r12, sp, #4
    add r2, sp, #20
    add r3, sp, #8
    mov r0, r4
    mov r1, r5
    str r12, [sp]
    bl native_fn_021e4744
    cmp r0, #0
    beq ov000_021e0944_L150
    cmp r6, #0
    add r1, sp, #8
    bne ov000_021e0944_L104
    cmp r5, #1
    ldreq r0, [sp, #0xc]
    ldr r2, [sp, #0x4]
    addeq r0, r0, #737280
    streq r0, [sp, #0xc]
    add r0, sp, #20
    bl native_fn_021e0898
    ldr r0, [sp, #0xc]
    mov r1, #1
    add r0, r0, #737280
    bl native_fn_021d84e8
    b ov000_021e0944_L150
ov000_021e0944_L104:
    cmp r6, #1
    bne ov000_021e0944_L138
    ldr r0, [sp, #0xc]
    ldr r2, [sp, #0x4]
    add r3, r0, #737280
    add r0, sp, #20
    str r3, [sp, #0xc]
    bl native_fn_021e0898
    ldr r0, [sp, #0xc]
    mov r1, #1
    add r0, r0, #737280
    bl native_fn_021d84e8
    b ov000_021e0944_L150
ov000_021e0944_L138:
    ldr r2, [sp, #0x4]
    add r0, sp, #20
    bl native_fn_021e0898
    ldr r0, [sp, #0xc]
    mov r1, #1
    bl native_fn_021d84e8
ov000_021e0944_L150:
    ldr r0, =0x022322d4
    mov r1, #0
    strb r1, [r0, #0x210]
    bl native_fn_0205c030
    mov r4, r0
    bl native_fn_0205bf3c
    cmp r0, #1
    cmpeq r4, #6
    beq ov000_021e0944_L1e8
    cmp r0, #1
    cmpeq r4, #5
    beq ov000_021e0944_L1e8
    ldr r0, =0x02232344
    ldr r1, =0x022324e4
    add r2, sp, #32
    mov r3, #1
    bl native_fn_021da5e4
    cmp r0, #0
    beq ov000_021e0944_L1c4
    ldr r0, =0x022324e4
    add r1, sp, #32
    bl native_fn_021dbbb8
    ldr r1, [sp, #0x20]
    ldr r0, =0x022322d4
    ldr r2, [sp, #0x24]
    str r1, [r0, #0x70]
    ldr r1, [sp, #0x28]
    str r2, [r0, #0x74]
    str r1, [r0, #0x78]
ov000_021e0944_L1c4:
    ldr r12, =0x02232344
    ldr r3, =0x0223238c
    ldmia r12, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r3, =0x022323e4
    ldmia r12, {r0, r1, r2}
    add sp, sp, #44
    stmia r3, {r0, r1, r2}
    ldmia sp!, {r3, r4, r5, r6, pc}
ov000_021e0944_L1e8:
    ldr r0, =0x02232344
    ldr r1, =0x022324e4
    mov r2, #1
    bl native_fn_021dae04
    add sp, sp, #44
    ldmia sp!, {r3, r4, r5, r6, pc}
}
