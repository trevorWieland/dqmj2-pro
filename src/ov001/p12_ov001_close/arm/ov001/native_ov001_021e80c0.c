/* ov001 row 0x021e80c0: 184 bytes.
 *
 * What it does: 46 instructions; 12 call(s) to 0x021e7d88, 0x021dccd0, 0x021db438, +9 more; loops (back edge at +0x04); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: loop with 12 calls (46 instructions, 12 calls, 2 branches, 11 back edges, 0 literal slots).
 *
 *   branch +0x50 -> +0x9c
 *   branch +0x5c -> +0x9c
 *   branch +0x74 -> +0x8c
 *   back edge +0x98 -> +0x68
 *   test +0x4c cmp r0, #0
 *   test +0x54 cmp r7, #0
 *   test +0x70 cmp r0, #0
 *   test +0x90 cmp r5, r7
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e80c0; the literal pool and
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

extern void native_fn_021e7d88(void);
extern void native_fn_021dccd0(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_mode_byte_021db530(void);
extern void native_fn_021e2afc(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021e7538(void);
extern void native_fn_021e7740(void);


asm u32 native_ov001_021e80c0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    bl native_fn_021e7d88
    mov r0, #0
    bl native_fn_021dccd0
    mov r0, #0
    mov r1, r0
    bl ov001_side_slot_record_021db438
    mov r8, r0
    mov r0, #1
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r9, r0
    mov r0, #0
    bl ov001_mode_byte_021db530
    mov r6, r0
    mov r0, #1
    bl ov001_mode_byte_021db530
    mov r7, r0
    bl native_fn_021e2afc
    cmp r0, #0
    bne ov001_021e80c0_L9c
    cmp r7, #0
    mov r5, #0
    ble ov001_021e80c0_L9c
    mov r10, r9
    mov r4, r5
ov001_021e80c0_L68:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021e80c0_L8c
    mov r0, r5
    mov r1, r9
    mov r2, r8
    mov r3, r4
    bl native_fn_021e7538
ov001_021e80c0_L8c:
    add r5, r5, #1
    cmp r5, r7
    add r10, r10, #1088
    blt ov001_021e80c0_L68
ov001_021e80c0_L9c:
    mov r0, r8
    mov r1, r6
    mov r2, r9
    mov r3, r7
    bl native_fn_021e7740
    add r0, r6, r7
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
