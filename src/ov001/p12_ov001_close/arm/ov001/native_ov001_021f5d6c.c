/* ov001 row 0x021f5d6c: 308 bytes.
 *
 * What it does: 75 instructions; 10 call(s) to 0x0202ac08, 0x021eea10, 0x0205d790, +7 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 10 calls (75 instructions, 10 calls, 10 branches, 10 back edges, 2 literal slots).
 *
 *   pool +0x12c -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x130 -> constant 0x0223992c (image word 0x0223992c)
 *   branch +0x14 -> +0x98
 *   branch +0x2c -> +0x44
 *   branch +0x5c -> +0x8c
 *   branch +0x94 -> +0x124
 *   branch +0x9c -> +0x124
 *   branch +0xac -> +0xe0
 *   branch +0xc0 -> +0xe0
 *   branch +0xd0 -> +0xe0
 *   branch +0xe4 -> +0x124
 *   branch +0x100 -> +0x114
 *   test +0x10 cmp r1, #0
 *   test +0x28 cmp r2, #0
 *   test +0x58 cmp r1, #0
 *   test +0x98 cmp r1, #10
 *   test +0xa8 cmp r1, #0
 *   test +0xbc cmp r0, #0
 *   test +0xcc cmp r0, #0
 *   test +0xe0 cmp r5, #0
 *   test +0xfc cmp r0, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f5d6c; the literal pool and
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

extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_021f5c38(void);
extern void native_fn_021f5cc0(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_021dc940(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021f5d6c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r4, r0
    ldrb r1, [r4, #0x327]
    mov r5, #0
    cmp r1, #0
    bne ov001_021f5d6c_L98
    ldr r0, =0x0223989c
    ldrsb r2, [r0, #68]
    add r1, r2, #1
    strb r1, [r0, #0x44]
    cmp r2, #0
    bne ov001_021f5d6c_L44
    ldr r0, =0x0223992c
    bl native_fn_0202ac08
    mov r0, #140
    mov r1, r5
    bl native_fn_021eea10
ov001_021f5d6c_L44:
    mov r0, #140
    bl native_fn_0205d790
    add r1, r4, #512
    ldrsb r1, [r1, #83]
    mov r2, r0
    cmp r1, #0
    beq ov001_021f5d6c_L8c
    mov r1, r4
    mov r0, #140
    bl ov001_effect_resource_create_021eec7c
    str r0, [r4, #0x338]
    mov r12, #1
    mov r0, r4
    mov r1, r4
    mov r2, #54
    mov r3, #0
    strb r12, [r4, #0x1ff]
    bl native_fn_021f5c38
ov001_021f5d6c_L8c:
    mov r0, #10
    strb r0, [r4, #0x327]
    b ov001_021f5d6c_L124
ov001_021f5d6c_L98:
    cmp r1, #10
    bne ov001_021f5d6c_L124
    add r1, r4, #512
    ldrsb r1, [r1, #83]
    cmp r1, #0
    beq ov001_021f5d6c_Le0
    mov r1, #54
    mov r5, #1
    bl native_fn_021f5cc0
    cmp r0, #0
    beq ov001_021f5d6c_Le0
    ldr r0, [r4, #0x338]
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_021f5d6c_Le0
    mov r0, r4
    mov r1, #39
    bl native_fn_021dc940
ov001_021f5d6c_Le0:
    cmp r5, #0
    bne ov001_021f5d6c_L124
    ldr r0, =0x0223989c
    ldrsb r1, [r0, #68]
    sub r1, r1, #1
    strb r1, [r0, #0x44]
    ldrsb r0, [r0, #68]
    cmp r0, #0
    bne ov001_021f5d6c_L114
    mov r0, #140
    bl native_fn_021eeb70
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
ov001_021f5d6c_L114:
    mov r0, #0
    strb r0, [r4, #0x327]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
ov001_021f5d6c_L124:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
