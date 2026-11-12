/* ov001 row 0x021f642c: 428 bytes.
 *
 * What it does: 103 instructions; 12 call(s) to 0x0207afec, 0x0202ac08, 0x021f6088, +9 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 12 calls (103 instructions, 12 calls, 7 branches, 10 back edges, 4 literal slots).
 *
 *   pool +0x19c -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x1a0 -> constant 0x0223992c (image word 0x0223992c)
 *   pool +0x1a4 -> constant 0x00000119 (image word 0x00000119)
 *   pool +0x1a8 -> constant 0x0000010d (image word 0x0000010d)
 *   branch +0x38 -> +0xd0
 *   branch +0x48 -> +0x60
 *   branch +0x88 -> +0xbc
 *   branch +0xdc -> +0x110
 *   branch +0xf4 -> +0x110
 *   branch +0x11c -> +0x154
 *   branch +0x160 -> +0x194
 *   branch +0x178 -> +0x188
 *   test +0x10 cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x40 cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   test +0xd8 cmp r1, #10
 *   test +0xf0 cmp r1, #40
 *   test +0x118 cmp r1, #20
 *   test +0x144 cmp r0, #0
 *   test +0x15c cmp r1, #100
 *   test +0x170 cmp r1, #0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f642c; the literal pool and
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
extern void native_fn_0202ac08(void);
extern void native_fn_021f6088(void);
extern void native_fn_021f2120(void);
extern void native_fn_0220f868(void);
extern void native_fn_021f2230(void);
extern void native_fn_021f4210(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021f642c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x84]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    ldr r0, =0x0223989c
    moveq r5, #1
    ldrh r0, [r0, #80]
    movne r5, #0
    bl native_fn_0207afec
    ldr r1, =0x0223989c
    mov r4, r0
    ldrb r0, [r1, #0x41]
    cmp r0, #0
    bne ov001_021f642c_Ld0
    ldrb r0, [r1, #0x10]
    cmp r0, #0
    ldrne r6, [r1, #0x80]
    bne ov001_021f642c_L60
    ldrh r0, [r4, #8]
    mov r0, r0, lsl #16
    movs r0, r0, lsr #28
    ldreq r6, [r1, #0x80]
    movne r6, #0
ov001_021f642c_L60:
    ldr r0, =0x0223992c
    bl native_fn_0202ac08
    ldr r0, =0x0223989c
    mov r1, r6
    ldrh r2, [r0, #80]
    ldr r0, [r0, #0x84]
    bl native_fn_021f6088
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    beq ov001_021f642c_Lbc
    mov r0, r6
    mov r1, #176
    bl native_fn_021f2120
    mov r0, r6
    mov r1, #249
    bl native_fn_021f2120
    ldr r1, =0x00000119
    mov r0, r6
    bl native_fn_021f2120
    ldr r1, =0x0000010d
    mov r0, r6
    bl native_fn_021f2120
ov001_021f642c_Lbc:
    ldr r0, =0x0223989c
    mov r1, #0
    strb r1, [r0, #0x40]
    mov r1, #10
    strb r1, [r0, #0x41]
ov001_021f642c_Ld0:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x41]
    cmp r1, #10
    bne ov001_021f642c_L110
    ldrb r1, [r0, #0x40]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0x40]
    cmp r1, #40
    bls ov001_021f642c_L110
    mov r0, r5
    bl native_fn_0220f868
    ldr r1, =0x0223989c
    mov r2, #20
    strb r0, [r1, #0x3f]
    strb r2, [r1, #0x41]
ov001_021f642c_L110:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x41]
    cmp r1, #20
    bne ov001_021f642c_L154
    ldrh r1, [r4, #8]
    mov r2, r5
    mov r1, r1, lsl #16
    movs r1, r1, lsr #28
    ldr r1, =0x0223989c
    ldreq r0, [r0, #0x80]
    ldrb r1, [r1, #0x3f]
    movne r0, #0
    bl native_fn_021f2230
    cmp r0, #0
    ldrne r0, =0x0223989c
    movne r1, #100
    strneb r1, [r0, #0x41]
ov001_021f642c_L154:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x41]
    cmp r1, #100
    bne ov001_021f642c_L194
    mov r1, #0
    strb r1, [r0, #0x41]
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    moveq r1, #27
    beq ov001_021f642c_L188
    bl native_fn_021f4210
    ldr r0, =0x0223989c
    mov r1, #3
ov001_021f642c_L188:
    strb r1, [r0, #0x1b]
    ldr r0, =0x0223992c
    bl native_fn_0202ac4c
ov001_021f642c_L194:
    mov r0, #0
    ldmia sp!, {r4, r5, r6, pc}
}
