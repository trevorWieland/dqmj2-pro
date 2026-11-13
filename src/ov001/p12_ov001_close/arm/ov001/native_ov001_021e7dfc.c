/* ov001 row 0x021e7dfc: 320 bytes.
 *
 * What it does: 80 instructions; 21 call(s) to 0x021e7d88, 0x021db438, 0x021db438, +18 more; loops (back edge at +0x04); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: loop with 21 calls (80 instructions, 21 calls, 3 branches, 17 back edges, 0 literal slots).
 *
 *   branch +0x48 -> +0x64
 *   branch +0x60 -> +0xc8
 *   branch +0x6c -> +0x94
 *   back edge +0x90 -> +0x74
 *   branch +0x9c -> +0x128
 *   back edge +0xc0 -> +0xa4
 *   branch +0xc4 -> +0x128
 *   branch +0xd0 -> +0xf8
 *   back edge +0xf4 -> +0xd8
 *   branch +0x100 -> +0x128
 *   back edge +0x124 -> +0x108
 *   test +0x44 cmp r0, #0
 *   test +0x5c cmp r1, r0
 *   test +0x64 cmp r4, #0
 *   test +0x8c cmp r9, r4
 *   test +0x94 cmp r5, #0
 *   test +0xbc cmp r9, r5
 *   test +0xc8 cmp r5, #0
 *   test +0xf0 cmp r9, r5
 *   test +0xf8 cmp r4, #0
 *   test +0x120 cmp r9, r4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e7dfc; the literal pool and
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
extern void ov001_side_slot_record_021db438(void);
extern void ov001_mode_byte_021db530(void);
extern void native_fn_020444ec(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa84c(void);
extern void native_fn_021e7538(void);
extern void native_fn_021e7740(void);


asm u32 native_ov001_021e7dfc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    bl native_fn_021e7d88
    mov r0, #0
    mov r1, r0
    bl ov001_side_slot_record_021db438
    mov r6, r0
    mov r0, #1
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r7, r0
    mov r0, #0
    bl ov001_mode_byte_021db530
    mov r4, r0
    mov r0, #1
    bl ov001_mode_byte_021db530
    mov r5, r0
    bl native_fn_020444ec
    cmp r0, #0
    beq ov001_021e7dfc_L64
    bl native_fn_01ffa824
    mov r8, r0
    bl native_fn_01ffa84c
    and r1, r8, #255
    cmp r1, r0
    bhs ov001_021e7dfc_Lc8
ov001_021e7dfc_L64:
    cmp r4, #0
    mov r9, #0
    ble ov001_021e7dfc_L94
    mov r8, r9
ov001_021e7dfc_L74:
    mov r0, r9
    mov r1, r6
    mov r2, r7
    mov r3, r8
    bl native_fn_021e7538
    add r9, r9, #1
    cmp r9, r4
    blt ov001_021e7dfc_L74
ov001_021e7dfc_L94:
    cmp r5, #0
    mov r9, #0
    ble ov001_021e7dfc_L128
    mov r8, r9
ov001_021e7dfc_La4:
    mov r0, r9
    mov r1, r7
    mov r2, r6
    mov r3, r8
    bl native_fn_021e7538
    add r9, r9, #1
    cmp r9, r5
    blt ov001_021e7dfc_La4
    b ov001_021e7dfc_L128
ov001_021e7dfc_Lc8:
    cmp r5, #0
    mov r9, #0
    ble ov001_021e7dfc_Lf8
    mov r8, r9
ov001_021e7dfc_Ld8:
    mov r0, r9
    mov r1, r7
    mov r2, r6
    mov r3, r8
    bl native_fn_021e7538
    add r9, r9, #1
    cmp r9, r5
    blt ov001_021e7dfc_Ld8
ov001_021e7dfc_Lf8:
    cmp r4, #0
    mov r9, #0
    ble ov001_021e7dfc_L128
    mov r8, r9
ov001_021e7dfc_L108:
    mov r0, r9
    mov r1, r6
    mov r2, r7
    mov r3, r8
    bl native_fn_021e7538
    add r9, r9, #1
    cmp r9, r4
    blt ov001_021e7dfc_L108
ov001_021e7dfc_L128:
    mov r0, r6
    mov r1, r4
    mov r2, r7
    mov r3, r5
    bl native_fn_021e7740
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
