/* ov001 row 0x0220c6e0: 268 bytes.
 *
 * What it does: 66 instructions; 9 call(s) to 0x02065d88, 0x021db438, 0x0220c7e0, +6 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 9 calls (66 instructions, 9 calls, 5 branches, 8 back edges, 1 literal slot).
 *
 *   pool +0x108 -> constant 0x51eb851f (image word 0x51eb851f)
 *   branch +0x24 -> +0x3c
 *   branch +0x48 -> +0x100
 *   branch +0x6c -> +0x84
 *   branch +0x80 -> +0x9c
 *   branch +0x8c -> +0x9c
 *   branch +0xa0 -> +0xf0
 *   back edge +0xfc -> +0x54
 *   test +0x1c cmp r0, #1
 *   test +0x44 cmp r9, #0
 *   test +0x5c cmp r0, #0
 *   test +0x64 cmpne r0, #0
 *   test +0x88 cmp r0, #0
 *   test +0x94 cmp r0, #1
 *   test +0x9c cmp r10, #0
 *   test +0xf4 cmp r8, r9
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220c6e0; the literal pool and
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

extern void native_fn_02065d88(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021dc4cc(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021db788(void);
extern void native_fn_022024d4(void);


asm u32 native_ov001_0220c6e0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r6, r0
    mov r0, r1
    mov r4, r2
    bl native_fn_02065d88
    mov r5, r0
    ldrb r0, [r5, #0x30]
    cmp r0, #1
    movne r9, #1
    bne ov001_0220c6e0_L3c
    mov r0, r4
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r6, r0
    mov r9, #3
ov001_0220c6e0_L3c:
    mov r8, #0
    mov r4, r8
    cmp r9, #0
    ble ov001_0220c6e0_L100
    mov r11, r8
    mov r7, r8
ov001_0220c6e0_L54:
    ldrb r0, [r6, #0x31c]
    mov r10, r7
    cmp r0, #0
    ldrneb r0, [r6, #0x1ff]
    cmpne r0, #0
    mov r0, r6
    beq ov001_0220c6e0_L84
    mov r1, #1
    mov r2, r7
    bl native_fn_021dc4cc
    mov r10, r0
    b ov001_0220c6e0_L9c
ov001_0220c6e0_L84:
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0220c6e0_L9c
    ldrb r0, [r5, #0x29]
    cmp r0, #1
    moveq r10, #1
ov001_0220c6e0_L9c:
    cmp r10, #0
    beq ov001_0220c6e0_Lf0
    ldrb r10, [r5, #0x2b]
    mov r0, r6
    bl native_fn_021dbcbc
    mul r2, r10, r0
    ldr r0, =0x51eb851f
    smull r1, r3, r0, r2
    mov r0, r2, lsr #31
    add r3, r0, r3, asr #5
    add r10, r3, #1
    mov r0, r6
    mov r1, r10
    bl native_fn_021db788
    ldrb r0, [r6, #0x31e]
    ldrb r1, [r6, #0x31f]
    rsb r2, r10, #0
    bl native_fn_022024d4
    add r0, r6, #768
    strh r11, [r0, #32]
    add r4, r4, #1
ov001_0220c6e0_Lf0:
    add r8, r8, #1
    cmp r8, r9
    add r6, r6, #1088
    blt ov001_0220c6e0_L54
ov001_0220c6e0_L100:
    mov r0, r4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
