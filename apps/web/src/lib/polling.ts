export function poll<T>(
  fn: () => Promise<T>,
  shouldContinue: (value: T) => boolean,
  intervalMs: number,
  onValue: (value: T) => void,
  onError?: (e: unknown) => void
) {
  let stopped = false;

  async function tick() {
    if (stopped) return;
    try {
      const v = await fn();
      onValue(v);
      if (shouldContinue(v)) {
        setTimeout(tick, intervalMs);
      }
    } catch (e) {
      onError?.(e);
      setTimeout(tick, intervalMs);
    }
  }

  tick();

  return () => {
    stopped = true;
  };
}
