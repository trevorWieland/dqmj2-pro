/* ov001 row 0x022046bc: 128 bytes.
 *
 * What it does: 32 instructions; 6 call(s) to 0x021db530, 0x02204724, 0x021db438, +3 more; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 6 calls (32 instructions, 6 calls, 2 branches, 5 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x68
 *   branch +0x48 -> +0x58
 *   branch +0x54 -> +0x5c
 *   back edge +0x64 -> +0x38
 *   test +0x20 cmp r10, #0
 *   test +0x28 cmp r6, #0
 *   test +0x44 cmp r9, #0
 *   test +0x50 cmp r0, #0
 *   test +0x60 cmp r5, r6
 *   test +0x68 cmp r8, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022046bc; the literal pool and
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

extern void ov001_mode_byte_021db530(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0220459c(void);


asm u32 native_ov001_022046bc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    mov r11, r1
    mov r9, r2
    mov r8, r3
    bl ov001_mode_byte_021db530
    mov r6, r0
    mov r7, #0
    cmp r10, #0
    orreq r7, r7, #1
    cmp r6, #0
    mov r5, #0
    ble ov001_022046bc_L68
    mov r4, #2
ov001_022046bc_L38:
    mov r0, r10
    mov r1, r5
    bl ov001_side_slot_record_021db438
    cmp r9, #0
    beq ov001_022046bc_L58
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_022046bc_L5c
ov001_022046bc_L58:
    orr r7, r7, r4, lsl r5
ov001_022046bc_L5c:
    add r5, r5, #1
    cmp r5, r6
    blt ov001_022046bc_L38
ov001_022046bc_L68:
    cmp r8, #0
    orrne r7, r7, #32
    mov r0, r11
    mov r1, r7
    bl native_fn_0220459c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
