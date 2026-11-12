/* ov001 row 0x0221b140: 276 bytes.
 *
 * What it does: 68 instructions; 11 call(s) to 0x021db8d0, 0x021dbd8c, 0x021dbd3c, +8 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (68 instructions, 11 calls, 2 branches, 11 back edges, 1 literal slot).
 *
 *   pool +0x110 -> constant 0x0000270f (image word 0x0000270f)
 *   branch +0x24 -> +0x74
 *   back edge +0x80 -> +0x18
 *   branch +0x98 -> +0xe8
 *   back edge +0xf4 -> +0x88
 *   test +0x20 cmp r0, #0
 *   test +0x68 cmp r7, r0, asr #2
 *   test +0x78 cmp r6, #3
 *   test +0x8c cmp r0, #0
 *   test +0x94 cmpne r0, #0
 *   test +0xdc cmp r8, r0, asr #2
 *   test +0xec cmp r6, #3
 *   test +0x100 cmp r8, r0, asr #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221b140; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbd8c(void);
extern void native_fn_021dbd3c(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021dbcf0(void);


asm u32 native_ov001_0221b140 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r9, [r0, #0x4]
    mov r8, #0
    ldr r7, =0x0000270f
    mov r6, r8
    mov r10, r9
ov001_0221b140_L18:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221b140_L74
    mov r0, r10
    bl native_fn_021dbd8c
    mov r5, r0
    mov r0, r10
    bl native_fn_021dbd3c
    mov r11, r0
    mov r0, r10
    bl native_fn_021dbcbc
    mov r4, r0
    mov r0, r10
    bl native_fn_021dbcf0
    add r0, r4, r0
    add r0, r11, r0
    add r1, r5, r0
    mov r0, r1, asr #1
    add r0, r1, r0, lsr #30
    cmp r7, r0, asr #2
    mov r0, r0, asr #2
    movgt r7, r0
ov001_0221b140_L74:
    add r6, r6, #1
    cmp r6, #3
    add r10, r10, #1088
    blt ov001_0221b140_L18
    mov r6, #0
ov001_0221b140_L88:
    ldrb r0, [r9, #0x31c]
    cmp r0, #0
    ldrneb r0, [r9, #0x1ff]
    cmpne r0, #0
    beq ov001_0221b140_Le8
    mov r0, r9
    bl native_fn_021dbd8c
    mov r5, r0
    mov r0, r9
    bl native_fn_021dbd3c
    mov r4, r0
    mov r0, r9
    bl native_fn_021dbcbc
    mov r10, r0
    mov r0, r9
    bl native_fn_021dbcf0
    add r0, r10, r0
    add r0, r4, r0
    add r1, r5, r0
    mov r0, r1, asr #1
    add r0, r1, r0, lsr #30
    cmp r8, r0, asr #2
    mov r0, r0, asr #2
    movlt r8, r0
ov001_0221b140_Le8:
    add r6, r6, #1
    cmp r6, #3
    add r9, r9, #1088
    blt ov001_0221b140_L88
    mov r0, r7, asr #1
    add r0, r7, r0, lsr #30
    cmp r8, r0, asr #2
    movle r0, #1
    movgt r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
