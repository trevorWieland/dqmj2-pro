package dev.dqmj2pro.dualsurface.native3;

import android.graphics.PixelFormat;
import android.graphics.Bitmap;
import android.view.PixelCopy;
import android.view.MotionEvent;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.widget.FrameLayout;

final class SurfacePanel extends FrameLayout implements SurfaceHolder.Callback {
    final int slot;
    final HostActivity host;
    final SurfaceView view;
    long token;
    SurfacePanel(HostActivity context, int role) {
        super(context);
        host = context;
        slot = role;
        setBackgroundColor(0xff101018);
        view = new SurfaceView(context);
        view.getHolder().setFormat(PixelFormat.RGBA_8888);
        view.getHolder().addCallback(this);
        addView(view, new LayoutParams(1, 1, android.view.Gravity.CENTER));
        view.setOnTouchListener((v, e) -> {
            if (e.getActionMasked() == MotionEvent.ACTION_DOWN || e.getActionMasked() == MotionEvent.ACTION_MOVE) {
                int x = (int)Math.floor(e.getX() * 256.0 / Math.max(1, view.getWidth()));
                int y = (int)Math.floor(e.getY() * 192.0 / Math.max(1, view.getHeight()));
                boolean accepted = NativeBridge.touch(slot, token, x, y);
                BridgeApp.event("TOUCH", "slot=" + slot + " logical=" + x + "," + y + " accepted=" + accepted);
                host.app().report();
            }
            return true;
        });
    }
    @Override protected void onMeasure(int widthSpec, int heightSpec) {
        int w = MeasureSpec.getSize(widthSpec), h = MeasureSpec.getSize(heightSpec);
        int width = Math.min(w, h * 4 / 3);
        int height = Math.min(h, width * 3 / 4);
        LayoutParams params = (LayoutParams)view.getLayoutParams();
        params.width = width;
        params.height = height;
        super.onMeasure(widthSpec, heightSpec);
    }
    @Override public void surfaceCreated(SurfaceHolder holder) {
        token = host.app().nextToken();
        boolean ok = NativeBridge.attach(slot, token, holder.getSurface());
        BridgeApp.event("ATTACH", "slot=" + slot + " token=" + token + " display=" + host.getDisplay().getDisplayId() + " accepted=" + ok);
    }
    @Override public void surfaceChanged(SurfaceHolder holder, int format, int w, int h) {
        NativeBridge.resize(slot, token, w, h, host.getDisplay().getRotation());
        BridgeApp.event("RESIZE", "slot=" + slot + " view=" + w + "x" + h + " rotation=" + host.getDisplay().getRotation());
        int[] origin = new int[2];
        view.getLocationOnScreen(origin);
        BridgeApp.event("VIEWPORT", "display=" + host.getDisplay().getDisplayId() + " slot=" + slot + " x=" + origin[0] + " y=" + origin[1] + " w=" + view.getWidth() + " h=" + view.getHeight());
        host.app().report();
    }
    @Override public void surfaceDestroyed(SurfaceHolder holder) {
        NativeBridge.detach(slot, token);
        BridgeApp.event("DETACH", "slot=" + slot + " token=" + token);
        host.app().report();
    }
    void capture() {
        Bitmap bitmap = Bitmap.createBitmap(256, 192, Bitmap.Config.ARGB_8888);
        PixelCopy.request(view, bitmap, result -> {
            if (result == PixelCopy.SUCCESS) {
                java.io.File file = new java.io.File(host.getFilesDir(), "capture-slot-" + slot + ".png");
                try (java.io.FileOutputStream stream = new java.io.FileOutputStream(file)) {
                    if (!bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)) throw new java.io.IOException("compress");
                    BridgeApp.event("OWNED_CAPTURE", "slot=" + slot + " result=0 bytes=" + file.length());
                } catch (java.io.IOException error) { BridgeApp.event("CAPTURE_FAILED", error.toString()); }
            } else BridgeApp.event("CAPTURE_FAILED", "slot=" + slot + " result=" + result);
            bitmap.recycle();
        }, host.app().handler);
    }
    void guardCheck() {
        boolean wrongToken = !NativeBridge.touch(slot, token - 1, 10, 10);
        boolean outside = !NativeBridge.touch(slot, token, -1, 192);
        boolean oldAttach = !NativeBridge.attach(slot, token - 1, view.getHolder().getSurface());
        NativeBridge.detach(slot, token - 1);
        BridgeApp.event("GUARD_CHECK", "slot=" + slot + " wrongToken=" + wrongToken + " outside=" + outside + " oldAttach=" + oldAttach);
    }
}
