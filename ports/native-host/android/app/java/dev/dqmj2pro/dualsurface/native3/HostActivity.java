package dev.dqmj2pro.dualsurface.native3;

import android.app.Activity;
import android.content.Intent;
import android.content.res.Configuration;
import android.os.Bundle;
import android.widget.LinearLayout;
import android.widget.TextView;

public abstract class HostActivity extends Activity {
    LinearLayout column;
    TextView label;
    boolean split;
    abstract int role();
    BridgeApp app() { return (BridgeApp)getApplication(); }
    @Override public void onCreate(Bundle saved) {
        super.onCreate(saved);
        setTurnScreenOn(true);
        setShowWhenLocked(true);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        getWindow().addFlags(android.view.WindowManager.LayoutParams.FLAG_FULLSCREEN);
        column = new LinearLayout(this);
        column.setOrientation(LinearLayout.VERTICAL);
        column.setBackgroundColor(0xff101018);
        label = new TextView(this);
        label.setTextColor(0xffffffff);
        label.setPadding(8, 4, 8, 4);
        column.addView(label);
        setContentView(column);
        displayMode(false);
        app().opened(this);
        command(getIntent());
    }
    void displayMode(boolean fallback) {
        if (column.getChildCount() > 1 && split == fallback) return;
        split = fallback;
        while (column.getChildCount() > 1) column.removeViewAt(1);
        column.addView(new SurfacePanel(this, role()), new LinearLayout.LayoutParams(-1, 0, 1));
        if (fallback && role() == 0) column.addView(new SurfacePanel(this, 1), new LinearLayout.LayoutParams(-1, 0, 1));
        label.setText("C7 native surface host | display " + getDisplay().getDisplayId() + " | " + (fallback ? "single-display fallback" : "dynamic dual display") + "\nSynthetic component only; not game rendering");
    }
    @Override protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        command(intent);
    }
    void capture() {
        for (int i = 1; i < column.getChildCount(); ++i) ((SurfacePanel)column.getChildAt(i)).capture();
    }
    void guardCheck() {
        for (int i = 1; i < column.getChildCount(); ++i) ((SurfacePanel)column.getChildAt(i)).guardCheck();
    }
    void command(Intent intent) {
        if (role() != 0 || intent == null) return;
        String action = intent.getStringExtra("command");
        if (action != null) app().command(action);
    }
    @Override protected void onStart() { super.onStart(); app().visible(1); }
    @Override protected void onStop() { app().visible(-1); super.onStop(); }
    @Override public void onConfigurationChanged(Configuration config) {
        super.onConfigurationChanged(config);
        column.requestLayout();
        BridgeApp.event("CONFIG", "role=" + role() + " display=" + getDisplay().getDisplayId() + " orientation=" + config.orientation);
    }
    @Override protected void onDestroy() { app().closed(this); super.onDestroy(); }
    @Override public void onBackPressed() {
        if (role() == 1) app().command("single");
        else finish();
    }
}
