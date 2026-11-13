/* ov001 row 0x0220bf30: 144 bytes.
 *
 * What it does: 36 instructions; 7 call(s) to 0x02065d88, 0x0220d468, 0x0220bf64, +4 more; loops (back edge at +0x10); returns through pop {r4, r5, r6, pc}
 *
 * Decoded shape: loop with 7 calls (36 instructions, 7 calls, 4 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x1c -> +0x88
 *   branch +0x3c -> +0x4c
 *   back edge +0x48 -> +0x34
 *   branch +0x50 -> +0x88
 *   branch +0x64 -> +0x88
 *   test +0x18 cmp r0, #2
 *   test +0x34 tst r0, r1, lsl r2
 *   test +0x44 cmp r2, #4
 *   test +0x4c cmp r3, #0
 *   test +0x60 cmp r4, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220bf30; the literal pool and
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
extern void native_fn_0220d468(void);
extern void native_fn_021d8dec(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void native_fn_021f1414(void);
extern void ov001_select_mode_id_021f1438(void);


asm u32 native_ov001_0220bf30 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r6, r0
    mov r5, r1
    mov r4, #0
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2c]
    cmp r0, #2
    bne ov001_0220bf30_L88
    mov r0, r6
    bl native_fn_0220d468
    mov r2, #1
    mov r3, r4
    mov r1, r2
ov001_0220bf30_L34:
    tst r0, r1, lsl r2
    movne r3, r2
    bne ov001_0220bf30_L4c
    add r2, r2, #1
    cmp r2, #4
    ble ov001_0220bf30_L34
ov001_0220bf30_L4c:
    cmp r3, #0
    beq ov001_0220bf30_L88
    mov r0, r3
    bl native_fn_021d8dec
    ldrh r4, [r0, #12]
    cmp r4, #0
    beq ov001_0220bf30_L88
    mov r0, #1
    mov r2, r4
    mov r3, r0
    mov r1, #0
    bl ov001_begin_state_transition_021f1354
    and r0, r5, #255
    bl native_fn_021f1414
    bl ov001_select_mode_id_021f1438
ov001_0220bf30_L88:
    mov r0, r4
    ldmia sp!, {r4, r5, r6, pc}
}
