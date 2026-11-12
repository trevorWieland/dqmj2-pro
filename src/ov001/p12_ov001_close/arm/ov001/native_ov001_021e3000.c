/* ov001 row 0x021e3000: 216 bytes.
 *
 * What it does: 50 instructions; 11 call(s) to 0x021dba58, 0x021dba58, 0x021dba58, +8 more; loops (back edge at +0x0c); returns through pop {r4, r5, r6, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 11 calls (50 instructions, 11 calls, 6 branches, 11 back edges, 4 literal slots).
 *
 *   pool +0xc8 -> native_data_0222ec00 (image word 0x0222ec00)
 *   pool +0xcc -> native_data_0222ec08 (image word 0x0222ec08)
 *   pool +0xd0 -> native_data_0222ec10 (image word 0x0222ec10)
 *   pool +0xd4 -> constant 0x02238ad0 (image word 0x02238ad0)
 *   branch +0x4c -> +0x6c
 *   branch +0x68 -> +0xa4
 *   branch +0x78 -> +0x88
 *   branch +0x84 -> +0xa4
 *   branch +0x8c -> +0x9c
 *   branch +0x98 -> +0xa4
 *   test +0x48 cmp r4, #0
 *   test +0x6c cmp r5, #0
 *   test +0x88 cmp r6, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e3000; the literal pool and
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

extern void native_fn_021dba58(void);
extern void native_fn_021dbac8(void);
extern void native_fn_021d732c(void);
extern void native_fn_021d7d4c(void);
extern void native_fn_021d7574(void);
extern u8 native_data_0222ec00[];
extern u8 native_data_0222ec08[];
extern u8 native_data_0222ec10[];
extern void native_fn_02041510(void);


asm u32 native_ov001_021e3000 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    mov r0, #0
    mov r1, r0
    bl native_fn_021dba58
    mov r0, #0
    mov r1, #1
    bl native_fn_021dba58
    mov r6, r0
    mov r0, #0
    mov r1, #2
    bl native_fn_021dba58
    mov r5, r0
    mov r0, #0
    bl native_fn_021dbac8
    mov r4, r0
    mov r0, #0
    mov r1, #2
    bl native_fn_021d732c
    cmp r4, #0
    beq ov001_021e3000_L6c
    mov r0, r4
    bl native_fn_021d7d4c
    mov r1, r0
    mov r0, #0
    mov r2, #1
    bl native_fn_021d7574
    b ov001_021e3000_La4
ov001_021e3000_L6c:
    cmp r5, #0
    mov r0, #0
    mov r2, #1
    beq ov001_021e3000_L88
    ldr r1, =native_data_0222ec00
    bl native_fn_021d7574
    b ov001_021e3000_La4
ov001_021e3000_L88:
    cmp r6, #0
    beq ov001_021e3000_L9c
    ldr r1, =native_data_0222ec08
    bl native_fn_021d7574
    b ov001_021e3000_La4
ov001_021e3000_L9c:
    ldr r1, =native_data_0222ec10
    bl native_fn_021d7574
ov001_021e3000_La4:
    mov r0, #0
    mov r1, #2
    mov r2, #15
    bl native_fn_02041510
    ldr r0, =0x02238ad0
    mov r1, #5
    strb r1, [r0, #0x3]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, pc}
}
