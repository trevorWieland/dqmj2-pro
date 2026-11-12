/* ov001 row 0x021f892c: 392 bytes.
 *
 * What it does: 96 instructions; 12 call(s) to 0x0207afec, 0x021f82d8, 0x0202ac08, +9 more; loops (back edge at +0x10); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (96 instructions, 12 calls, 5 branches, 12 back edges, 2 literal slots).
 *
 *   pool +0x180 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x184 -> constant 0x0223992c (image word 0x0223992c)
 *   branch +0x24 -> +0x94
 *   branch +0x34 -> +0x80
 *   branch +0x98 -> +0xc4
 *   branch +0xc8 -> +0x11c
 *   branch +0x120 -> +0x148
 *   test +0x20 cmp r0, #0
 *   test +0x30 cmp r4, #0
 *   test +0x94 cmp r0, #10
 *   test +0xa4 cmp r0, #0
 *   test +0xc4 cmp r0, #20
 *   test +0x11c cmp r0, #30
 *   test +0x138 cmp r0, #15
 *   test +0x148 cmp r0, #100
 *   0 block transfer(s), 11 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f892c; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_021f82d8(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021f892c (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    ldr r0, =0x0223989c
    ldrh r0, [r0, #80]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    ldrsh r4, [r0, #12]
    ldrsb r0, [r1, #72]
    cmp r0, #0
    bne ov001_021f892c_L94
    ldr r0, [r1, #0x78]
    bl native_fn_021f82d8
    cmp r4, #0
    beq ov001_021f892c_L80
    ldr r0, =0x0223992c
    bl native_fn_0202ac08
    mov r0, r4
    mov r1, #0
    bl native_fn_021eea10
    mov r0, r4
    bl native_fn_0205d790
    ldr r1, =0x0223989c
    mov r2, r0
    ldr r1, [r1, #0x78]
    mov r0, r4
    bl native_fn_021eec7c
    ldr r1, =0x0223989c
    mov r2, #10
    str r0, [r1, #0x7c]
    strb r2, [r1, #0x48]
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
ov001_021f892c_L80:
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x48]
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
ov001_021f892c_L94:
    cmp r0, #10
    bne ov001_021f892c_Lc4
    ldr r0, [r1, #0x7c]
    bl native_fn_0205d6f4
    cmp r0, #0
    addne sp, sp, #4
    ldmneia sp!, {r3, r4, pc}
    ldr r0, =0x0223989c
    mov r1, #20
    strb r1, [r0, #0x48]
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
ov001_021f892c_Lc4:
    cmp r0, #20
    bne ov001_021f892c_L11c
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    mov r4, r0
    ldrh r0, [r1, #80]
    bl native_fn_0207afec
    mov r3, #0
    str r3, [sp]
    ldr r12, =0x0223989c
    ldrsh r2, [r0, #16]
    ldrb r1, [r4, #0x21]
    ldr r0, [r12, #0x78]
    bl native_fn_021dbf98
    ldr r0, =0x0223989c
    mov r1, #30
    strb r1, [r0, #0x48]
    mov r1, #0
    strb r1, [r0, #0x22]
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
ov001_021f892c_L11c:
    cmp r0, #30
    bne ov001_021f892c_L148
    ldrsb r0, [r1, #34]
    add sp, sp, #4
    add r0, r0, #1
    strb r0, [r1, #0x22]
    ldrsb r0, [r1, #34]
    cmp r0, #15
    movgt r0, #100
    strgtb r0, [r1, #0x48]
    ldmia sp!, {r3, r4, pc}
ov001_021f892c_L148:
    cmp r0, #100
    addne sp, sp, #4
    ldmneia sp!, {r3, r4, pc}
    mov r0, r4
    bl native_fn_021eeb70
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x48]
    mov r1, #27
    strb r1, [r0, #0x1b]
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
