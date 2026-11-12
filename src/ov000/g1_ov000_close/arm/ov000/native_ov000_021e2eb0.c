/* ov000 row 0x021e2eb0: 376 bytes.
 *
 * What it does: 92 instructions; 20 call(s) to 0x0205c030, 0x0205bf3c, 0x021e3180, +17 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x170 -> constant 0x022322d4 (image word 0x022322d4)
 *   pool +0x174 -> constant 0x022322c4 (image word 0x022322c4)
 *   branch +0x38 -> +0x90
 *   branch +0x40 -> +0x90
 *   branch +0x74 -> +0x84
 *   branch +0x80 -> +0x168
 *   branch +0x8c -> +0x168
 *   branch +0x94 -> +0xec
 *   branch +0x9c -> +0xec
 *   branch +0xd0 -> +0xe0
 *   branch +0xdc -> +0x168
 *   branch +0xe8 -> +0x168
 *   branch +0xf0 -> +0x148
 *   branch +0xfc -> +0x124
 *   branch +0x120 -> +0x168
 *   branch +0x144 -> +0x168
 *   test +0x34 cmp r4, #6
 *   test +0x3c cmp r5, #2
 *   test +0x70 cmp r0, #7
 *   test +0x90 cmp r4, #5
 *   test +0x98 cmp r5, #2
 *   test +0xcc cmp r0, #5
 *   test +0xec cmp r5, #5
 *   test +0xf8 cmp r0, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e2eb0; the literal pool and
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

extern void native_fn_0205c030(void);
extern void native_fn_0205bf3c(void);
extern void native_fn_021e3180(void);
extern void native_fn_021e07f0(void);
extern void native_fn_0205c050(void);
extern void native_fn_021e53cc(void);
extern void native_fn_021e0d78(void);
extern void native_fn_021e52d4(void);
extern void native_fn_0205c070(void);


asm u32 native_ov000_021e2eb0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r1, =0x022322d4
    mov r3, #0
    strb r3, [r1, #0x27f]
    mov r2, #1
    ldr r0, =0x022322c4
    strb r2, [r1, #0x1e3]
    str r3, [r0, #0x8]
    bl native_fn_0205c030
    mov r4, r0
    bl native_fn_0205bf3c
    mov r5, r0
    bl native_fn_021e3180
    cmp r4, #6
    bne ov000_021e2eb0_L90
    cmp r5, #2
    beq ov000_021e2eb0_L90
    mov r0, #6
    bl native_fn_021e07f0
    bl native_fn_0205c050
    ldr r1, =0x022322d4
    strb r0, [r1, #0x1e0]
    mov r0, r1
    bl native_fn_021e53cc
    ldr r0, =0x022322d4
    mov r1, #1
    ldrb r0, [r0, #0x1e0]
    mov r2, #0
    cmp r0, #7
    bne ov000_021e2eb0_L84
    mov r0, #31
    bl native_fn_021e0d78
    b ov000_021e2eb0_L168
ov000_021e2eb0_L84:
    mov r0, #34
    bl native_fn_021e0d78
    b ov000_021e2eb0_L168
ov000_021e2eb0_L90:
    cmp r4, #5
    bne ov000_021e2eb0_Lec
    cmp r5, #2
    beq ov000_021e2eb0_Lec
    mov r0, #5
    bl native_fn_021e07f0
    bl native_fn_0205c050
    ldr r1, =0x022322d4
    strb r0, [r1, #0x1e0]
    mov r0, r1
    bl native_fn_021e52d4
    ldr r0, =0x022322d4
    mov r1, #1
    ldrb r0, [r0, #0x1e0]
    mov r2, #0
    cmp r0, #5
    bne ov000_021e2eb0_Le0
    mov r0, #10
    bl native_fn_021e0d78
    b ov000_021e2eb0_L168
ov000_021e2eb0_Le0:
    mov r0, #13
    bl native_fn_021e0d78
    b ov000_021e2eb0_L168
ov000_021e2eb0_Lec:
    cmp r5, #5
    bne ov000_021e2eb0_L148
    bl native_fn_0205c070
    cmp r0, #0
    beq ov000_021e2eb0_L124
    mov r0, #4
    bl native_fn_021e07f0
    mov r1, #1
    ldr r3, =0x022322d4
    mov r2, r1
    mov r0, #3
    strb r1, [r3, #0x27e]
    bl native_fn_021e0d78
    b ov000_021e2eb0_L168
ov000_021e2eb0_L124:
    mov r0, #2
    bl native_fn_021e07f0
    mov r0, #1
    ldr r3, =0x022322d4
    mov r1, r0
    mov r2, r0
    strb r0, [r3, #0x27e]
    bl native_fn_021e0d78
    b ov000_021e2eb0_L168
ov000_021e2eb0_L148:
    mov r0, #2
    bl native_fn_021e07f0
    mov r0, #1
    ldr r3, =0x022322d4
    mov r1, r0
    mov r2, r0
    strb r0, [r3, #0x27e]
    bl native_fn_021e0d78
ov000_021e2eb0_L168:
    mov r0, #0
    ldmia sp!, {r3, r4, r5, pc}
}
