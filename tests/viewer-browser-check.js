// Run with Playwright's browser_run_code_unsafe filename argument against the
// local Studio server. Instrumentation exists only in this disposable test page.
async (page) => {
  const errors = [];
  page.on('pageerror', error => errors.push(String(error)));
  await page.unroute('**/viewer.js?*');
  await page.route('**/viewer.js?*', async route => {
    const response = await route.fetch({ url: 'http://localhost:8001/viewer.js' });
    const source = await response.text();
    await route.fulfill({ contentType: 'text/javascript', body: source + `
      const originalInit = TrajectoryViewer.prototype.init;
      TrajectoryViewer.prototype.init = function() {
        originalInit.call(this);
        window.__testViewer = this;
        window.__renderCount = 0;
        const render = this.renderer.render.bind(this.renderer);
        this.renderer.render = (...args) => { window.__renderCount++; return render(...args); };
      };` });
  });
  await page.goto('about:blank');
  await page.goto('http://localhost:8001/collections/barilla-curobo-smooth-production-20260913/index.html#ca5b5bb5875c40b466aec21cb14a23657496bb0a935f240a822dd5220e9032e3-curobo');
  await page.waitForFunction(() => window.__testViewer?.trajectoryPoints.length > 2);
  const result = await page.evaluate(async () => {
    const v = window.__testViewer;
    const frames = async n => { for (let i = 0; i < n; i++) await new Promise(requestAnimationFrame); };
    const results = {};
    const check = async (name, action, expectedDraws) => {
      const before = window.__renderCount;
      action();
      await frames(120);
      const end = window.__renderCount;
      await frames(30);
      const draws = end - before, settledDraws = window.__renderCount - end;
      if ((expectedDraws ? draws < 1 : draws !== 0) || settledDraws !== 0)
        throw new Error(`${name}: draws=${draws}, settled=${settledDraws}`);
      results[name] = { draws, settledDraws };
    };
    await frames(120);
    await check('idle', () => {}, false);
    document.querySelector('#btn-play-pause').click();
    const start = window.__renderCount;
    await frames(30);
    document.querySelector('#btn-play-pause').click();
    results.playback = window.__renderCount - start;
    if (results.playback < 2) throw new Error('Playback did not render');
    await frames(5);
    await check('paused', () => {}, false);
    await check('zoom', () => v.canvas.dispatchEvent(new WheelEvent('wheel', { deltaY: -100, cancelable: true })), true);
    await check('orbit', () => { v.camera.position.x += 0.2; v.controls.update(); }, true);
    await check('scrub', () => {
      const slider = document.querySelector('#timeline-slider');
      slider.value = 500; slider.dispatchEvent(new Event('input', { bubbles: true }));
    }, true);
    await check('resize', () => v.onResize(), true);
    await check('edit', () => v.setEditMode(true), true);
    await check('handleMovement', () => {
      v.controlSpheres[0].position.x += .01;
      v.transformControls[0].dispatchEvent({ type: 'change' });
    }, true);
    await check('leaveEdit', () => v.setEditMode(false), true);
    await check('clearPath', () => v.drawTrajectoryPath([]), true);
    return results;
  });
  if (errors.length) throw new Error(errors.join('\n'));
  return { ...result, pageErrors: errors };
}
