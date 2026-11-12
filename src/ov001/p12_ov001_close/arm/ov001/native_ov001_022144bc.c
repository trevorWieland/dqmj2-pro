/* ov001 row 0x022144bc: 468 bytes.
 *
 * What it does: 115 instructions; 13 call(s) to 0x0207afec, 0x0202ac08, 0x021eea10, +10 more; loops (back edge at +0x10); returns through pop {r3, r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (115 instructions, 13 calls, 16 branches, 13 back edges, 2 literal slots).
 *
 *   pool +0x1cc -> constant 0x02242b50 (image word 0x02242b50)
 *   pool +0x1d0 -> constant 0x02242b64 (image word 0x02242b64)
 *   branch +0x24 -> +0x54
 *   branch +0x2c -> +0x44
 *   branch +0x50 -> +0x1c0
 *   branch +0x58 -> +0xec
 *   branch +0x6c -> +0x1c0
 *   branch +0xa0 -> +0xdc
 *   branch +0xd8 -> +0x1c0
 *   branch +0xe8 -> +0x1c0
 *   branch +0xf0 -> +0x114
 *   branch +0x110 -> +0x1c0
 *   branch +0x118 -> +0x144
 *   branch +0x140 -> +0x1c0
 *   branch +0x148 -> +0x16c
 *   branch +0x168 -> +0x1c0
 *   branch +0x170 -> +0x1c0
 *   branch +0x180 -> +0x19c
 *   test +0x20 cmp r0, #0
 *   test +0x28 cmp r4, #0
 *   test +0x54 cmp r0, #5
 *   test +0x68 cmp r0, #0
 *   test +0x9c cmp r4, #0
 *   test +0xec cmp r0, #10
 *   test +0x104 cmp r0, #30
 *   test +0x114 cmp r0, #20
 *   test +0x144 cmp r0, #30
 *   test +0x15c cmp r0, #30
 *   test +0x16c cmp r0, #100
 *   test +0x17c cmp r4, #0
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022144bc; the literal pool and
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
extern void native_fn_021eea10(void);
extern void native_fn_021eeff0(void);
extern void native_fn_021dbf98(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021ee91c(void);
extern void native_fn_0205d718(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_021f14a4(void);
extern void native_fn_02202568(void);


asm u32 native_ov001_022144bc (register u32 a0)
{
    stmdb sp!, {r3, r4, lr}
    sub sp, sp, #4
    ldr r0, =0x02242b50
    ldrh r0, [r0, #12]
    bl native_fn_0207afec
    ldr r1, =0x02242b50
    ldrsh r4, [r0, #12]
    ldrsb r0, [r1]
    cmp r0, #0
    bne ov001_022144bc_L54
    cmp r4, #0
    beq ov001_022144bc_L44
    ldr r0, =0x02242b64
    bl native_fn_0202ac08
    mov r0, r4
    mov r1, #0
    bl native_fn_021eea10
ov001_022144bc_L44:
    ldr r0, =0x02242b50
    mov r1, #5
    strb r1, [r0]
    b ov001_022144bc_L1c0
ov001_022144bc_L54:
    cmp r0, #5
    bne ov001_022144bc_Lec
    ldr r2, [r1, #0x10]
    add r0, r2, #256
    ldrsb r0, [r0, #228]
    cmp r0, #0
    bne ov001_022144bc_L1c0
    ldrb r0, [r2, #0x31e]
    ldrh r1, [r1, #12]
    bl native_fn_021eeff0
    mov r2, #1
    mov r1, #8
    ldr r3, =0x02242b50
    str r2, [sp]
    mov r2, r0
    ldr r0, [r3, #0x10]
    sub r3, r1, #9
    bl native_fn_021dbf98
    cmp r4, #0
    beq ov001_022144bc_Ldc
    mov r0, r4
    bl native_fn_0205d790
    ldr r1, =0x02242b50
    mov r2, r0
    ldr r1, [r1, #0x10]
    mov r0, r4
    bl native_fn_021eec7c
    ldr r1, =0x02242b50
    mov r2, #0
    strb r0, [r1, #0xa]
    strb r2, [r1, #0x1]
    mov r0, #10
    strb r0, [r1]
    b ov001_022144bc_L1c0
ov001_022144bc_Ldc:
    ldr r0, =0x02242b50
    mov r1, #20
    strb r1, [r0]
    b ov001_022144bc_L1c0
ov001_022144bc_Lec:
    cmp r0, #10
    bne ov001_022144bc_L114
    ldrsb r0, [r1, #1]
    add r0, r0, #1
    strb r0, [r1, #0x1]
    ldrsb r0, [r1, #1]
    cmp r0, #30
    movge r0, #20
    strgeb r0, [r1]
    b ov001_022144bc_L1c0
ov001_022144bc_L114:
    cmp r0, #20
    bne ov001_022144bc_L144
    ldr r0, [r1, #0x10]
    add r1, r0, #512
    ldrsb r1, [r1, #52]
    bl native_fn_021ee91c
    ldr r0, =0x02242b50
    mov r1, #30
    strb r1, [r0]
    mov r1, #0
    strb r1, [r0, #0x1]
    b ov001_022144bc_L1c0
ov001_022144bc_L144:
    cmp r0, #30
    bne ov001_022144bc_L16c
    ldrsb r0, [r1, #1]
    add r0, r0, #1
    strb r0, [r1, #0x1]
    ldrsb r0, [r1, #1]
    cmp r0, #30
    movge r0, #100
    strgeb r0, [r1]
    b ov001_022144bc_L1c0
ov001_022144bc_L16c:
    cmp r0, #100
    bne ov001_022144bc_L1c0
    mov r0, #0
    strb r0, [r1]
    cmp r4, #0
    beq ov001_022144bc_L19c
    ldrb r0, [r1, #0xa]
    bl native_fn_0205d718
    mov r0, r4
    bl native_fn_021eeb70
    ldr r0, =0x02242b64
    bl native_fn_0202ac4c
ov001_022144bc_L19c:
    ldr r0, =0x02242b50
    mov r1, #5
    strb r1, [r0, #0x2]
    bl native_fn_021f14a4
    ldr r0, =0x02242b50
    ldr r1, [r0, #0x10]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_02202568
ov001_022144bc_L1c0:
    mov r0, #0
    add sp, sp, #4
    ldmia sp!, {r3, r4, pc}
}
