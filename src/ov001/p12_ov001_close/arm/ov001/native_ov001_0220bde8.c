/* ov001 row 0x0220bde8: 328 bytes.
 *
 * What it does: 79 instructions; 13 call(s) to 0x02065d88, 0x021db438, 0x021db438, +10 more; loops (back edge at +0x18); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 13 calls (79 instructions, 13 calls, 5 branches, 11 back edges, 3 literal slots).
 *
 *   pool +0x13c -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0x140 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x144 -> constant 0x55555556 (image word 0x55555556)
 *   branch +0x28 -> +0x40
 *   branch +0x3c -> +0x50
 *   branch +0x58 -> +0x134
 *   branch +0x70 -> +0x124
 *   branch +0x84 -> +0x124
 *   branch +0x9c -> +0xb4
 *   branch +0xb0 -> +0xc0
 *   back edge +0x130 -> +0x68
 *   test +0x20 cmp r0, #1
 *   test +0x50 cmp r7, #0
 *   test +0x6c cmp r0, #0
 *   test +0x80 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0x128 cmp r6, r7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220bde8; the literal pool and
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
extern void native_fn_0220bb7c(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_021d96d4(void);


asm u32 native_ov001_0220bde8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r2
    mov r5, r0
    mov r0, r10
    mov r4, r1
    mov r8, #0
    bl native_fn_02065d88
    ldrb r0, [r0, #0x30]
    cmp r0, #1
    mov r0, r5
    bne ov001_0220bde8_L40
    mov r1, r8
    bl ov001_side_slot_record_021db438
    mov r9, r0
    mov r7, #3
    b ov001_0220bde8_L50
ov001_0220bde8_L40:
    mov r1, r4
    bl ov001_side_slot_record_021db438
    mov r9, r0
    mov r7, #1
ov001_0220bde8_L50:
    cmp r7, #0
    mov r6, #0
    ble ov001_0220bde8_L134
    ldr r5, =0x020d3fe0
    ldr r4, =0x0b60b60b
    ldr r11, =0x55555556
ov001_0220bde8_L68:
    ldrb r0, [r9, #0x31c]
    cmp r0, #0
    beq ov001_0220bde8_L124
    mov r0, r9
    mov r1, r10
    bl native_fn_0220bb7c
    cmp r0, #0
    beq ov001_0220bde8_L124
    add r0, r9, #768
    ldrsh r0, [r0, #32]
    mov r0, r0, lsl #5
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov001_0220bde8_Lb4
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_0220bde8_Lc0
ov001_0220bde8_Lb4:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_0220bde8_Lc0:
    bl native_fn_020259b4
    umull r8, r3, r0, r4
    adds r1, r8, #0
    mov r1, #182
    mla r3, r0, r1, r3
    mov r2, r0, asr #31
    mla r3, r2, r4, r3
    mov r0, #2048
    adc r0, r3, r0
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    add r0, r5, r0, lsl #2
    ldrsh r1, [r0, #2]
    mov r0, r9
    rsb r1, r1, #0
    add r1, r1, #4096
    mov r1, r1, asr #8
    mov r2, r1, lsl #1
    smull r1, r3, r11, r2
    add r3, r3, r2, lsr #31
    add r1, r3, #4
    and r1, r1, #255
    bl native_fn_021d96d4
    mov r8, #1
ov001_0220bde8_L124:
    add r6, r6, #1
    cmp r6, r7
    add r9, r9, #1088
    blt ov001_0220bde8_L68
ov001_0220bde8_L134:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
