/* ov001 row 0x021feeb4: 252 bytes.
 *
 * What it does: 62 instructions; 9 call(s) to 0x02202360, 0x021db530, 0x021fef90, +6 more; loops (back edge at +0x28); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (62 instructions, 9 calls, 4 branches, 6 back edges, 1 literal slot).
 *
 *   pool +0xf8 -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x38 -> +0xdc
 *   branch +0x98 -> +0xac
 *   branch +0xa8 -> +0xbc
 *   branch +0xb8 -> +0xc8
 *   back edge +0xd8 -> +0x3c
 *   back edge +0xec -> +0x24
 *   test +0x34 cmp r8, #0
 *   test +0x60 cmp r3, #0
 *   test +0x6c cmpne r1, #0
 *   test +0x74 cmp r3, #0
 *   test +0x7c cmpne r0, #0
 *   test +0x88 cmp r10, #0
 *   test +0x94 cmpeq r0, r7
 *   test +0x9c cmp r10, #1
 *   test +0xa4 cmpeq r0, r7
 *   test +0xd0 cmp r8, r0, asr #24
 *   test +0xe8 cmp r10, #2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021feeb4; the literal pool and
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

extern void native_fn_02202360(void);
extern void native_fn_021db530(void);
extern void native_fn_021fd074(void);
extern void native_fn_021db438(void);
extern void native_fn_021ff000(void);
extern void native_fn_021fefb0(void);
extern void native_fn_02048308(void);


asm u32 native_ov001_021feeb4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_02202360
    mov r10, #0
    mov r4, #1
    mov r6, r0
    mov r11, r4
    mov r5, r10
ov001_021feeb4_L24:
    mov r0, r10
    bl native_fn_021db530
    mov r8, r0
    mov r7, #0
    cmp r8, #0
    ble ov001_021feeb4_Ldc
ov001_021feeb4_L3c:
    mov r0, r10
    mov r1, r7
    bl native_fn_021fd074
    mov r9, r0
    mov r0, r10
    mov r1, r7
    bl native_fn_021db438
    ldrb r3, [r0, #0x31c]
    mov r2, r5
    cmp r3, #0
    ldrne r1, [r0, #0x1e8]
    ldrneb r1, [r1, #0xac]
    cmpne r1, #0
    movne r2, r4
    cmp r3, #0
    ldrneb r0, [r0, #0x1ff]
    cmpne r0, #0
    movne r0, r11
    moveq r0, #0
    cmp r10, #0
    orr r2, r0, r2
    ldreqsb r0, [r6, #8]
    cmpeq r0, r7
    beq ov001_021feeb4_Lac
    cmp r10, #1
    ldreqsb r0, [r6, #10]
    cmpeq r0, r7
    bne ov001_021feeb4_Lbc
ov001_021feeb4_Lac:
    ldrsb r0, [r9, #12]
    mov r1, r2
    bl native_fn_021ff000
    b ov001_021feeb4_Lc8
ov001_021feeb4_Lbc:
    ldrsb r1, [r9, #12]
    mov r0, r10
    bl native_fn_021fefb0
ov001_021feeb4_Lc8:
    add r0, r7, #1
    mov r0, r0, lsl #24
    cmp r8, r0, asr #24
    mov r7, r0, asr #24
    bgt ov001_021feeb4_L3c
ov001_021feeb4_Ldc:
    add r0, r10, #1
    mov r0, r0, lsl #24
    mov r10, r0, asr #24
    cmp r10, #2
    blt ov001_021feeb4_L24
    bl native_fn_02048308
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
