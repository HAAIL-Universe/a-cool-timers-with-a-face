import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useKeyboard, UseKeyboardOptions } from '../hooks/useKeyboard';

describe('useKeyboard', () => {
  let onSpace: ReturnType<typeof vi.fn>;
  let onR: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    onSpace = vi.fn();
    onR = vi.fn();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('space key triggers onSpace callback', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: true,
    };

    renderHook(() => useKeyboard(options));

    const event = new KeyboardEvent('keydown', {
      code: 'Space',
      bubbles: true,
    });

    act(() => {
      window.dispatchEvent(event);
    });

    expect(onSpace).toHaveBeenCalledOnce();
    expect(onR).not.toHaveBeenCalled();
  });

  it('r key triggers onR callback', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: true,
    };

    renderHook(() => useKeyboard(options));

    const event = new KeyboardEvent('keydown', {
      code: 'KeyR',
      bubbles: true,
    });

    act(() => {
      window.dispatchEvent(event);
    });

    expect(onR).toHaveBeenCalledOnce();
    expect(onSpace).not.toHaveBeenCalled();
  });

  it('disabled option suppresses callbacks', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: false,
    };

    renderHook(() => useKeyboard(options));

    const spaceEvent = new KeyboardEvent('keydown', {
      code: 'Space',
      bubbles: true,
    });

    const rEvent = new KeyboardEvent('keydown', {
      code: 'KeyR',
      bubbles: true,
    });

    act(() => {
      window.dispatchEvent(spaceEvent);
      window.dispatchEvent(rEvent);
    });

    expect(onSpace).not.toHaveBeenCalled();
    expect(onR).not.toHaveBeenCalled();
  });

  it('other keys do not trigger callbacks', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: true,
    };

    renderHook(() => useKeyboard(options));

    const enterEvent = new KeyboardEvent('keydown', {
      code: 'Enter',
      bubbles: true,
    });

    act(() => {
      window.dispatchEvent(enterEvent);
    });

    expect(onSpace).not.toHaveBeenCalled();
    expect(onR).not.toHaveBeenCalled();
  });

  it('multiple space key presses trigger multiple callbacks', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: true,
    };

    renderHook(() => useKeyboard(options));

    const event = new KeyboardEvent('keydown', {
      code: 'Space',
      bubbles: true,
    });

    act(() => {
      window.dispatchEvent(event);
      window.dispatchEvent(event);
    });

    expect(onSpace).toHaveBeenCalledTimes(2);
  });

  it('prevents default behavior on space key', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: true,
    };

    renderHook(() => useKeyboard(options));

    const event = new KeyboardEvent('keydown', {
      code: 'Space',
      bubbles: true,
      cancelable: true,
    });

    const preventDefaultSpy = vi.spyOn(event, 'preventDefault');

    act(() => {
      window.dispatchEvent(event);
    });

    expect(preventDefaultSpy).toHaveBeenCalled();
  });

  it('prevents default behavior on r key', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: true,
    };

    renderHook(() => useKeyboard(options));

    const event = new KeyboardEvent('keydown', {
      code: 'KeyR',
      bubbles: true,
      cancelable: true,
    });

    const preventDefaultSpy = vi.spyOn(event, 'preventDefault');

    act(() => {
      window.dispatchEvent(event);
    });

    expect(preventDefaultSpy).toHaveBeenCalled();
  });

  it('cleanup removes event listener on unmount', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: true,
    };

    const { unmount } = renderHook(() => useKeyboard(options));

    unmount();

    const event = new KeyboardEvent('keydown', {
      code: 'Space',
      bubbles: true,
    });

    act(() => {
      window.dispatchEvent(event);
    });

    expect(onSpace).not.toHaveBeenCalled();
  });

  it('re-enables callbacks when enabled changes from false to true', () => {
    const options: UseKeyboardOptions = {
      onSpace,
      onR,
      enabled: false,
    };

    const { rerender } = renderHook((opts) => useKeyboard(opts), {
      initialProps: options,
    });

    const event = new KeyboardEvent('keydown', {
      code: 'Space',
      bubbles: true,
    });

    act(() => {
      window.dispatchEvent(event);
    });

    expect(onSpace).not.toHaveBeenCalled();

    rerender({
      onSpace,
      onR,
      enabled: true,
    });

    act(() => {
      window.dispatchEvent(event);
    });

    expect(onSpace).toHaveBeenCalledOnce();
  });
});
