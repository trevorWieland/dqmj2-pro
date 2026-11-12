/* ov001 row 0x021fa290: 416 bytes.
 *
 * What it does: 102 instructions; 20 call(s) to 0x021dbcbc, 0x021fa2c4, 0x02025a28, +17 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 20 calls (102 instructions, 20 calls, 10 branches, 18 back edges, 2 literal slots).
 *
 *   pool +0x198 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x19c -> constant 0x45800000 (image word 0x45800000)
 *   branch +0x1c -> +0x34
 *   branch +0x30 -> +0x40
 *   branch +0x58 -> +0x70
 *   branch +0x6c -> +0x7c
 *   branch +0xbc -> +0xdc
 *   branch +0xd8 -> +0x160
 *   branch +0xe0 -> +0x100
 *   branch +0xfc -> +0x160
 *   branch +0x104 -> +0x128
 *   branch +0x124 -> +0x160
 *   branch +0x130 -> +0x14c
 *   branch +0x148 -> +0x160
 *   test +0x14 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0xa4 cmp r2, #1
 *   test +0xb8 cmp r0, #200
 *   test +0xdc cmp r0, #300
 *   test +0x100 cmp r0, #400
 *   test +0x128 cmp r0, #500
 *   test +0x180 cmp r0, #0
 *   test +0x18c cmp r0, #1000
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fa290; the literal pool and
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

extern void native_fn_021dbcbc(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_021dbd24(void);
extern void native_fn_0200235c(void);
extern void native_fn_02026144(void);
extern void native_fn_02025578(void);


asm u32 native_ov001_021fa290 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r5, r1
    mov r0, r5
    mov r6, r2
    bl native_fn_021dbcbc
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov001_021fa290_L34
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021fa290_L40
ov001_021fa290_L34:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021fa290_L40:
    bl native_fn_020259b4
    mov r4, r0
    mov r0, r5
    bl native_fn_021dbd24
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov001_021fa290_L70
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021fa290_L7c
ov001_021fa290_L70:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021fa290_L7c:
    bl native_fn_020259b4
    sub r0, r4, r0
    add r1, r4, r4, lsl #1
    bl native_fn_0200235c
    ldr r5, [r5, #0x1e8]
    add r4, r0, #4096
    ldrb r0, [r5, #0xa6]
    ldrsh r2, [r5, #46]
    mul r1, r6, r0
    mov r0, #10
    cmp r2, #1
    mul r0, r1, r0
    movlt r2, #1
    add r1, r2, r2, lsl #1
    bl native_fn_02026144
    cmp r0, #200
    bgt ov001_021fa290_Ldc
    mov r1, #10
    mul r1, r0, r1
    ldr r2, =0x66666667
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #2
    b ov001_021fa290_L160
ov001_021fa290_Ldc:
    cmp r0, #300
    bgt ov001_021fa290_L100
    ldr r1, =0x66666667
    mov r2, r0, lsl #3
    smull r0, r3, r1, r2
    mov r0, r2, lsr #31
    add r3, r0, r3, asr #2
    add r3, r3, #40
    b ov001_021fa290_L160
ov001_021fa290_L100:
    cmp r0, #400
    bgt ov001_021fa290_L128
    mov r1, #6
    mul r1, r0, r1
    ldr r2, =0x66666667
    mov r0, r1, lsr #31
    smull r1, r3, r2, r1
    add r3, r0, r3, asr #2
    add r3, r3, #100
    b ov001_021fa290_L160
ov001_021fa290_L128:
    cmp r0, #500
    ldr r1, =0x66666667
    bgt ov001_021fa290_L14c
    mov r2, r0, lsl #2
    smull r0, r3, r1, r2
    mov r0, r2, lsr #31
    add r3, r0, r3, asr #2
    add r3, r3, #180
    b ov001_021fa290_L160
ov001_021fa290_L14c:
    mov r2, r0, lsl #1
    smull r0, r3, r1, r2
    mov r0, r2, lsr #31
    add r3, r0, r3, asr #2
    add r3, r3, #280
ov001_021fa290_L160:
    mul r0, r3, r4
    ldrb r1, [r5, #0xa7]
    add r1, r1, #1
    bl native_fn_02026144
    bl native_fn_02025a28
    ldr r1, =0x45800000
    bl native_fn_02025578
    bl native_fn_020259b4
    cmp r0, #0
    movlt r0, #0
    ldmltia sp!, {r4, r5, r6, pc}
    cmp r0, #1000
    movgt r0, #1000
    ldmia sp!, {r4, r5, r6, pc}
}
