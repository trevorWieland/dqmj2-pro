/* ov001 row 0x02213bac: 204 bytes.
 *
 * What it does: 49 instructions; 6 call(s) to 0x021db438, 0x021db530, 0x02213c68, +3 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill (49 instructions, 6 calls, 2 branches, 5 back edges, 2 literal slots).
 *
 *   pool +0xc4 -> constant 0x02242aac (image word 0x02242aac)
 *   pool +0xc8 -> constant 0x02242ab4 (image word 0x02242ab4)
 *   branch +0x50 -> +0xbc
 *   branch +0x70 -> +0xa8
 *   branch +0x7c -> +0xa8
 *   back edge +0xb8 -> +0x64
 *   test +0x20 cmp r0, #0
 *   test +0x48 cmp r0, #0
 *   test +0x6c cmp r0, #0
 *   test +0x78 tst r10, r0
 *   test +0xb0 cmp r4, r0
 *   1 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02213bac; the literal pool and
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

extern void ov001_side_slot_record_021db438(void);
extern void ov001_mode_byte_021db530(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0220fe50(void);


asm u32 native_ov001_02213bac (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r4, =0x02242aac
    mov r10, r0
    ldr r0, [r4, #0x4]
    mov r9, r1
    ldrb r0, [r0, #0x31e]
    mov r1, #0
    mov r11, r2
    cmp r0, #0
    moveq r4, #1
    movne r4, #0
    mov r0, r4
    mov r8, r3
    bl ov001_side_slot_record_021db438
    mov r5, r0
    mov r0, r4
    bl ov001_mode_byte_021db530
    str r0, [sp]
    cmp r0, #0
    mov r4, #0
    ble ov001_02213bac_Lbc
    ldr r1, =0x02242ab4
    mov r0, #12
    mla r6, r8, r0, r1
    mvn r7, r10
ov001_02213bac_L64:
    mov r0, r5
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_02213bac_La8
    ldr r0, [r5, #0x33c]
    tst r10, r0
    beq ov001_02213bac_La8
    stmia r6, {r5, r9}
    mov r0, r10
    strb r11, [r6, #0x9]
    bl native_fn_0220fe50
    strb r0, [r6, #0x8]
    ldr r0, [r5, #0x33c]
    add r6, r6, #12
    and r0, r0, r7
    str r0, [r5, #0x33c]
    add r8, r8, #1
ov001_02213bac_La8:
    ldr r0, [sp]
    add r4, r4, #1
    cmp r4, r0
    add r5, r5, #1088
    blt ov001_02213bac_L64
ov001_02213bac_Lbc:
    mov r0, r8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
