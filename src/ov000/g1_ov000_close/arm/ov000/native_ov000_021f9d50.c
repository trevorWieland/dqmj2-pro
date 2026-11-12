/* ov000 row 0x021f9d50: 160 bytes.
 *
 * What it does: 40 instructions; 15 call(s) to 0x02215698, 0x02088e8c, 0x021f9cdc, +12 more; loops (back edge at +0x0c); returns through pop {r3, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x14 -> +0x40
 *   branch +0x3c -> +0x90
 *   test +0x10 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f9d50; the literal pool and
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

extern void ov000_display_context_02215698(void);
extern void native_fn_02088e8c(void);
extern void native_fn_021f9cdc(void);
extern void native_fn_021e7b9c(void);
extern void native_fn_021f8b0c(void);
extern void native_fn_0204075c(void);
extern void native_fn_0221573c(void);
extern void native_fn_02214fc8(void);
extern void native_fn_022156a4(void);
extern void native_fn_0221570c(void);
extern void native_fn_02062074(void);
extern void native_fn_02061934(void);
extern void native_fn_020406a8(void);
extern void native_fn_0205e814(void);


asm u32 native_ov000_021f9d50 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    bl ov000_display_context_02215698
    mov r0, #0
    bl native_fn_02088e8c
    cmp r0, #0
    beq ov000_021f9d50_L40
    mov r3, #1
    mov r0, #5
    mov r1, #6
    mov r2, #35
    str r3, [sp]
    bl native_fn_021f9cdc
    mov r0, #82
    bl native_fn_021e7b9c
    bl native_fn_021f8b0c
    b ov000_021f9d50_L90
ov000_021f9d50_L40:
    mov r0, #9
    bl native_fn_0204075c
    mov r0, #11
    bl native_fn_0221573c
    mov r0, #2
    bl native_fn_02214fc8
    mov r0, #127
    bl native_fn_022156a4
    mov r0, #1
    bl native_fn_0221570c
    mov r0, #0
    bl native_fn_02062074
    mov r0, #2
    bl native_fn_02061934
    mov r0, #0
    bl native_fn_020406a8
    mov r0, #0
    mov r1, r0
    mov r2, #15
    bl native_fn_0205e814
ov000_021f9d50_L90:
    mov r0, #1
    bl native_fn_0221570c
    mov r0, #0
    ldmia sp!, {r3, pc}
}
