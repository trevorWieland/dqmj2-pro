/* ov001 row 0x02201bc0: 160 bytes.
 *
 * What it does: 39 instructions; 11 call(s) to 0x02041814, 0x021fe74c, 0x021fe9b0, +8 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, r7, r8, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (39 instructions, 11 calls, 1 branch, 10 back edges, 1 literal slot).
 *
 *   pool +0x9c -> constant 0x02239c10 (image word 0x02239c10)
 *   branch +0x34 -> +0x80
 *   back edge +0x7c -> +0x44
 *   test +0x08 cmp r0, #1
 *   test +0x30 cmp r0, #0
 *   test +0x78 cmp r0, r4, asr #24
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02201bc0; the literal pool and
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

extern void native_fn_02041814(void);
extern void native_fn_021fe74c(void);
extern void native_fn_021fe9b0(void);
extern void native_fn_0220b70c(void);
extern void native_fn_021db530(void);
extern void native_fn_021fd074(void);
extern void native_fn_0206d114(void);
extern void native_fn_021fdc08(void);
extern void native_fn_021fd354(void);


asm u32 native_ov001_02201bc0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    bl native_fn_02041814
    cmp r0, #1
    mov r0, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    bl native_fn_021fe74c
    bl native_fn_021fe9b0
    mov r0, #1
    bl native_fn_0220b70c
    mov r0, #1
    mov r8, #0
    bl native_fn_021db530
    cmp r0, #0
    ble ov001_02201bc0_L80
    mov r7, #1
    mov r6, r8
    mov r5, r7
ov001_02201bc0_L44:
    mov r0, r7
    mov r1, r8
    bl native_fn_021fd074
    ldrsb r0, [r0, #12]
    mov r1, r6
    bl native_fn_0206d114
    mov r0, r8
    bl native_fn_021fdc08
    add r0, r8, #1
    mov r4, r0, lsl #24
    mov r0, r5
    mov r8, r4, asr #24
    bl native_fn_021db530
    cmp r0, r4, asr #24
    bgt ov001_02201bc0_L44
ov001_02201bc0_L80:
    mov r0, #2
    bl native_fn_021fd354
    ldr r0, =0x02239c10
    mov r1, #16
    strb r1, [r0, #0xa]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
