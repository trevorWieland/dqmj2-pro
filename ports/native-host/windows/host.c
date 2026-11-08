#define UNICODE
#define _UNICODE
#define _WIN32_WINNT 0x0a00
#include <windows.h>
#include <windowsx.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <wchar.h>
#include "host_session.h"

static J2pHostSession session;
static HWND windows[2];
static uint8_t pixels[2][256 * 192 * 4];
static uint32_t paints[2], rejected, created;
static int failed, live;

static RECT viewport(HWND window) {
    RECT client, result = {0};
    int width, height;
    GetClientRect(window, &client);
    width = client.right; height = client.bottom;
    if (width <= 0 || height <= 0) return result;
    if ((int64_t)width * 192 > (int64_t)height * 256) width = height * 256 / 192;
    else height = width * 192 / 256;
    result.left = (client.right - width) / 2;
    result.top = (client.bottom - height) / 2;
    result.right = result.left + width; result.bottom = result.top + height;
    return result;
}

static void touch(HWND window, int x, int y) {
    RECT view = viewport(window);
    if (view.right <= view.left || view.bottom <= view.top || x < view.left || x >= view.right ||
        y < view.top || y >= view.bottom) { ++rejected; return; }
    if (!j2p_host_touch(&session, (x - view.left) * 256 / (view.right - view.left),
        (y - view.top) * 192 / (view.bottom - view.top))) failed = 1;
    InvalidateRect(windows[0], NULL, FALSE);
    InvalidateRect(windows[1], NULL, FALSE);
}

static void paint(HWND window, uint32_t slot) {
    PAINTSTRUCT paint_state;
    BITMAPINFO info = {0};
    RECT view = viewport(window), client;
    HDC dc = BeginPaint(window, &paint_state);
    uint32_t i;
    if (!dc) { failed = 1; return; }
    GetClientRect(window, &client);
    FillRect(dc, &client, (HBRUSH)GetStockObject(BLACK_BRUSH));
    if (!j2p_host_render(&session, slot, pixels[slot], sizeof(pixels[slot]), 256, 192, 1024)) failed = 1;
    for (i = 0; i < sizeof(pixels[slot]); i += 4) {
        uint8_t red = pixels[slot][i]; pixels[slot][i] = pixels[slot][i + 2]; pixels[slot][i + 2] = red;
    }
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = 256; info.bmiHeader.biHeight = -192;
    info.bmiHeader.biPlanes = 1; info.bmiHeader.biBitCount = 32; info.bmiHeader.biCompression = BI_RGB;
    if (view.right > view.left && view.bottom > view.top) {
        int copied = StretchDIBits(dc, view.left, view.top, view.right - view.left, view.bottom - view.top,
            0, 0, 256, 192, pixels[slot], &info, DIB_RGB_COLORS, SRCCOPY);
        if (copied == (int)GDI_ERROR) failed = 1;
        else ++paints[slot];
    }
    EndPaint(window, &paint_state);
}

static LRESULT CALLBACK procedure(HWND window, UINT message, WPARAM wparam, LPARAM lparam) {
    uintptr_t stored = (uintptr_t)GetWindowLongPtrW(window, GWLP_USERDATA);
    uint32_t slot = stored ? (uint32_t)(stored - 1) : 0;
    if (message == WM_NCCREATE) {
        CREATESTRUCTW *creation = (CREATESTRUCTW *)lparam;
        SetWindowLongPtrW(window, GWLP_USERDATA, (LONG_PTR)((uintptr_t)creation->lpCreateParams + 1));
        return TRUE;
    }
    if (message == WM_PAINT) { paint(window, slot); return 0; }
    if (message == WM_ERASEBKGND) return 1;
    if (message == WM_SIZE) { InvalidateRect(window, NULL, FALSE); return 0; }
    if (message == WM_LBUTTONDOWN || (message == WM_MOUSEMOVE && (wparam & MK_LBUTTON))) {
        touch(window, GET_X_LPARAM(lparam), GET_Y_LPARAM(lparam)); return 0;
    }
    if (message == WM_DPICHANGED) {
        RECT *suggested = (RECT *)lparam;
        SetWindowPos(window, NULL, suggested->left, suggested->top, suggested->right - suggested->left,
            suggested->bottom - suggested->top, SWP_NOZORDER | SWP_NOACTIVATE);
        return 0;
    }
    if (message == WM_TIMER) {
        j2p_host_step(&session);
        InvalidateRect(windows[0], NULL, FALSE); InvalidateRect(windows[1], NULL, FALSE);
        return 0;
    }
    if (message == WM_CLOSE) {
        uint32_t i;
        for (i = 0; i < 2; ++i) if (IsWindow(windows[i])) DestroyWindow(windows[i]);
        return 0;
    }
    if (message == WM_DESTROY) { KillTimer(window, 1); --live; if (!live) PostQuitMessage(0); return 0; }
    return DefWindowProcW(window, message, wparam, lparam);
}

static int open_windows(HINSTANCE instance) {
    uint32_t i;
    for (i = 0; i < 2; ++i) {
        windows[i] = CreateWindowExW(0, L"J2pNativeHost", i ? L"DQMJ2 Pro native host - lower" : L"DQMJ2 Pro native host - upper",
            WS_OVERLAPPEDWINDOW, 100 + (int)i * 550, 100, 530, 450, NULL, NULL, instance, (void *)(uintptr_t)i);
        if (!windows[i]) return 0;
        ++live; ++created;
        ShowWindow(windows[i], SW_SHOWNOACTIVATE); UpdateWindow(windows[i]);
    }
    return 1;
}

static int smoke(void) {
    RECT view;
    J2pHostSession before = session;
    MSG message;
    int x, y, wanted_x, wanted_y;
    if (j2p_host_touch(&session, -1, 0) || memcmp(&before, &session, sizeof(session))) return 0;
    if (!SetWindowPos(windows[1], NULL, 650, 100, 521, 680, SWP_NOZORDER | SWP_NOACTIVATE)) return 0;
    view = viewport(windows[1]);
    if (view.top <= 0) return 0;
    SendMessageW(windows[1], WM_LBUTTONDOWN, MK_LBUTTON, MAKELPARAM(0, 0));
    if (session.touches != before.touches || !rejected) return 0;
    x = view.left + (view.right - view.left) * 3 / 4;
    y = view.top + (view.bottom - view.top) / 4;
    wanted_x = (x - view.left) * 256 / (view.right - view.left);
    wanted_y = (y - view.top) * 192 / (view.bottom - view.top);
    SendMessageW(windows[1], WM_LBUTTONDOWN, MK_LBUTTON, MAKELPARAM(x, y));
    if (session.x != wanted_x || session.y != wanted_y || session.touches != before.touches + 1 ||
        session.state.matrices[1][12] != (wanted_x - 128) * 32 ||
        session.state.matrices[1][13] != (wanted_y - 96) * 4096 / 96) return 0;
    j2p_host_step(&session);
    UpdateWindow(windows[0]); UpdateWindow(windows[1]);
    while (PeekMessageW(&message, NULL, 0, 0, PM_REMOVE)) {
        if (message.message != WM_QUIT) { TranslateMessage(&message); DispatchMessageW(&message); }
    }
    return paints[0] && paints[1] && !failed && memcmp(pixels[0], pixels[1], sizeof(pixels[0])) != 0;
}

static int capture(HWND window, uint32_t slot) {
    RECT client;
    BITMAPINFO info = {0};
    BITMAPFILEHEADER header = {0};
    WCHAR path[MAX_PATH], *name;
    HDC source, memory;
    HBITMAP bitmap;
    HGDIOBJ previous;
    HANDLE file;
    void *data;
    DWORD written, bytes;
    int passed;
    GetClientRect(window, &client);
    if (client.right <= 0 || client.bottom <= 0 || client.right > 4096 || client.bottom > 4096) return 0;
    if (!GetModuleFileNameW(NULL, path, MAX_PATH) || !(name = wcsrchr(path, L'\\'))) return 0;
    ++name;
    if (swprintf(name, MAX_PATH - (size_t)(name - path), L"native-%lu-slot%u.bmp", GetCurrentProcessId(), slot) < 0) return 0;
    bytes = (DWORD)client.right * (DWORD)client.bottom * 4;
    info.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
    info.bmiHeader.biWidth = client.right; info.bmiHeader.biHeight = -client.bottom;
    info.bmiHeader.biPlanes = 1; info.bmiHeader.biBitCount = 32; info.bmiHeader.biCompression = BI_RGB;
    source = GetDC(window);
    if (!source) return 0;
    memory = CreateCompatibleDC(source);
    if (!memory) { ReleaseDC(window, source); return 0; }
    bitmap = CreateDIBSection(source, &info, DIB_RGB_COLORS, &data, NULL, 0);
    if (!bitmap) { DeleteDC(memory); ReleaseDC(window, source); return 0; }
    previous = SelectObject(memory, bitmap);
    passed = BitBlt(memory, 0, 0, client.right, client.bottom, source, 0, 0, SRCCOPY) != 0;
    file = passed ? CreateFileW(path, GENERIC_WRITE, 0, NULL, CREATE_NEW, FILE_ATTRIBUTE_NORMAL, NULL) : INVALID_HANDLE_VALUE;
    header.bfType = 0x4d42; header.bfOffBits = sizeof(header) + sizeof(info.bmiHeader); header.bfSize = header.bfOffBits + bytes;
    passed = file != INVALID_HANDLE_VALUE && WriteFile(file, &header, sizeof(header), &written, NULL) && written == sizeof(header) &&
        WriteFile(file, &info.bmiHeader, sizeof(info.bmiHeader), &written, NULL) && written == sizeof(info.bmiHeader) &&
        WriteFile(file, data, bytes, &written, NULL) && written == bytes;
    if (file != INVALID_HANDLE_VALUE && !CloseHandle(file)) passed = 0;
    SelectObject(memory, previous);
    if (!DeleteObject(bitmap) || !DeleteDC(memory) || !ReleaseDC(window, source)) passed = 0;
    return passed;
}

int main(int argc, char **argv) {
    WNDCLASSEXW klass = {0};
    HINSTANCE instance = GetModuleHandleW(NULL);
    MSG message;
    int capturing = argc == 2 && !strcmp(argv[1], "--smoke-capture"), passed = 1;
    int testing = capturing || (argc == 2 && !strcmp(argv[1], "--smoke"));
    uint32_t i;
    if (!SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2) &&
        !AreDpiAwarenessContextsEqual(GetThreadDpiAwarenessContext(), DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)) return 4;
    if (!j2p_host_init(&session)) return 2;
    klass.cbSize = sizeof(klass); klass.hInstance = instance; klass.lpfnWndProc = procedure;
    klass.lpszClassName = L"J2pNativeHost"; klass.hCursor = LoadCursorW(NULL, IDC_ARROW);
    if (!RegisterClassExW(&klass) || !open_windows(instance)) return 3;
    if (testing) {
        passed = smoke();
        if (capturing && passed) for (i = 0; i < 2; ++i) if (!capture(windows[i], i)) passed = 0;
    }
    else {
        if (!SetTimer(windows[0], 1, 16, NULL)) passed = 0;
        while (passed && GetMessageW(&message, NULL, 0, 0) > 0) { TranslateMessage(&message); DispatchMessageW(&message); }
    }
    for (i = 0; i < 2; ++i) if (IsWindow(windows[i])) DestroyWindow(windows[i]);
    passed = passed && !live && !IsWindow(windows[0]) && !IsWindow(windows[1]) && !failed;
    if (!UnregisterClassW(L"J2pNativeHost", instance)) passed = 0;
    printf("{\"passed\":%s,\"createdWindows\":%u,\"paints\":[%u,%u],\"touches\":%llu,\"rejectedMarginInputs\":%u,\"frames\":%llu,\"remainingWindows\":%d,\"gameplayClaim\":false}\n",
        passed ? "true" : "false", created, paints[0], paints[1], (unsigned long long)session.touches,
        rejected, (unsigned long long)session.frames, live);
    return passed ? 0 : 1;
}
