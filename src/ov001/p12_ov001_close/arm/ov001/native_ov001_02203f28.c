/* ov001 row 0x02203f28: 360 bytes.
 *
 * What it does: 90 instructions; 12 call(s) to 0x021db438, 0x021db508, 0x020692b0, +9 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (90 instructions, 12 calls, 2 branches, 12 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0xa8
 *   back edge +0xb0 -> +0x18
 *   branch +0xdc -> +0x154
 *   back edge +0x15c -> +0xc4
 *   test +0x2c cmp r0, #0
 *   test +0x3c cmp r0, #0
 *   test +0x44 cmpne r0, #0
 *   test +0x50 cmp r10, #0
 *   test +0xac cmp r9, #3
 *   test +0xd8 cmp r0, #0
 *   test +0xe8 cmp r0, #0
 *   test +0xf0 cmpne r0, #0
 *   test +0xfc cmp r10, #0
 *   test +0x158 cmp r6, #3
 *   2 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02203f28; the literal pool and
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

extern void native_fn_021db438(void);
extern void native_fn_021db508(void);
extern void native_fn_020692b0(void);
extern void native_fn_021fefb0(void);
extern void native_fn_02044cdc(void);


asm u32 native_ov001_02203f28 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r5, #0
    mov r9, r5
    mov r4, r5
    mov r11, r5
ov001_02203f28_L18:
    mov r0, r11
    mov r1, r9
    bl native_fn_021db438
    mov r6, r0
    ldr r0, [r6, #0x1e8]
    cmp r0, #0
    beq ov001_02203f28_La8
    ldrb r0, [r6, #0x31c]
    mov r1, r9
    cmp r0, #0
    ldrneb r0, [r6, #0x1ff]
    cmpne r0, #0
    movne r10, #1
    moveq r10, #0
    cmp r10, #0
    moveq r7, #6
    moveq r8, #9
    movne r7, #12
    movne r8, r7
    mov r0, #0
    bl native_fn_021db508
    stmia sp, {r4, r7, r8}
    mov r1, r4
    mov r2, r4
    and r3, r5, #255
    bl native_fn_020692b0
    mov r1, r0
    add r0, r6, #768
    ldrsb r0, [r0, #30]
    mov r2, r10
    bl native_fn_021fefb0
    ldr r0, [r6, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r5, r5, r0
ov001_02203f28_La8:
    add r9, r9, #1
    cmp r9, #3
    blt ov001_02203f28_L18
    mov r5, #0
    mov r6, r5
    mov r4, r5
    mov r11, #2
ov001_02203f28_Lc4:
    mov r0, r11
    mov r1, r6
    bl native_fn_021db438
    mov r7, r0
    ldr r0, [r7, #0x1e8]
    cmp r0, #0
    beq ov001_02203f28_L154
    ldrb r0, [r7, #0x31c]
    mov r1, r6
    cmp r0, #0
    ldrneb r0, [r7, #0x1ff]
    cmpne r0, #0
    movne r10, #1
    moveq r10, #0
    cmp r10, #0
    moveq r8, #6
    moveq r9, #9
    movne r8, #12
    movne r9, r8
    mov r0, #2
    bl native_fn_021db508
    stmia sp, {r4, r8, r9}
    mov r1, #1
    mov r2, r4
    and r3, r5, #255
    bl native_fn_020692b0
    mov r1, r0
    add r0, r7, #768
    ldrsb r0, [r0, #30]
    mov r2, r10
    bl native_fn_021fefb0
    ldr r0, [r7, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    add r0, r0, #1
    add r5, r5, r0
ov001_02203f28_L154:
    add r6, r6, #1
    cmp r6, #3
    blt ov001_02203f28_Lc4
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
