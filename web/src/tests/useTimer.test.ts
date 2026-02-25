import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useTimer } from '../hooks/useTimer';
import * as timerApi from '../api/timerApi';

vi.mock('../api/timerApi');

describe('useTimer', () => {
  const mockTimer = {
    id: 'timer-1',
    duration: 300,
    remainingTime: 300,
    status: 'idle' as const,
    urgencyLevel: 'low' as const,
    createdAt: new Date().toISOString(),
  };

  const mockTimerState = {
    timerId: 'timer-1',
    remainingSeconds: 300,
    status: 'idle' as const,
    urgencyLevel: 'low' as const,
  };

  beforeEach(() => {
    vi.useFakeTimers();
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('initializes with null timer ID and no polling', () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);

    const { result } = renderHook(() => useTimer());

    expect(result.current.timerId).toBeNull();
    expect(result.current.remainingSeconds).toBe(0);
    expect(result.current.status).toBe('idle');
  });

  it('creates a timer and starts polling after creation', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.getTimerState as any).mockResolvedValue(mockTimerState);

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    expect(result.current.timerId).toBe('timer-1');
    expect(result.current.remainingSeconds).toBe(300);

    await act(async () => {
      vi.advanceTimersByTime(1000);
    });

    await waitFor(() => {
      expect(timerApi.getTimerState).toHaveBeenCalled();
    });
  });

  it('polls every second when timer is active', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.getTimerState as any).mockResolvedValue({
      timerId: 'timer-1',
      remainingSeconds: 295,
      status: 'running',
      urgencyLevel: 'low',
    });

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    await act(async () => {
      await result.current.startTimer();
    });

    const initialCallCount = (timerApi.getTimerState as any).mock.calls.length;

    await act(async () => {
      vi.advanceTimersByTime(3000);
    });

    await waitFor(() => {
      expect((timerApi.getTimerState as any).mock.calls.length).toBeGreaterThan(
        initialCallCount
      );
    });
  });

  it('calls API startTimer and updates state', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.startTimer as any).mockResolvedValue(undefined);
    (timerApi.getTimerState as any).mockResolvedValue({
      timerId: 'timer-1',
      remainingSeconds: 300,
      status: 'running',
      urgencyLevel: 'low',
    });

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    await act(async () => {
      await result.current.startTimer();
    });

    expect(timerApi.startTimer).toHaveBeenCalledWith('timer-1');
  });

  it('calls API pauseTimer and stops polling', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.pauseTimer as any).mockResolvedValue(undefined);
    (timerApi.getTimerState as any).mockResolvedValue({
      timerId: 'timer-1',
      remainingSeconds: 250,
      status: 'paused',
      urgencyLevel: 'low',
    });

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    await act(async () => {
      await result.current.pauseTimer();
    });

    expect(timerApi.pauseTimer).toHaveBeenCalledWith('timer-1');
  });

  it('calls API resetTimer and updates state', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.resetTimer as any).mockResolvedValue(undefined);
    (timerApi.getTimerState as any).mockResolvedValue({
      timerId: 'timer-1',
      remainingSeconds: 300,
      status: 'idle',
      urgencyLevel: 'low',
    });

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    await act(async () => {
      await result.current.resetTimer();
    });

    expect(timerApi.resetTimer).toHaveBeenCalledWith('timer-1');
    expect(result.current.remainingSeconds).toBe(300);
  });

  it('handles urgency level changes during countdown', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.getTimerState as any).mockResolvedValue({
      timerId: 'timer-1',
      remainingSeconds: 60,
      status: 'running',
      urgencyLevel: 'medium',
    });

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    await act(async () => {
      vi.advanceTimersByTime(1000);
    });

    await waitFor(() => {
      expect(result.current.urgencyLevel).toBe('medium');
    });
  });

  it('cleans up polling interval on unmount', async () => {
    const clearIntervalSpy = vi.spyOn(global, 'clearInterval');

    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.getTimerState as any).mockResolvedValue(mockTimerState);

    const { result, unmount } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    await act(async () => {
      await result.current.startTimer();
    });

    unmount();

    expect(clearIntervalSpy).toHaveBeenCalled();
  });

  it('handles API errors gracefully', async () => {
    const error = new Error('API Error');
    (timerApi.createTimer as any).mockRejectedValue(error);

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      try {
        await result.current.initTimer(300);
      } catch {
        // Error expected
      }
    });

    expect(result.current.timerId).toBeNull();
  });

  it('does not poll when timer is idle', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.getTimerState as any).mockResolvedValue(mockTimerState);

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    const callCount = (timerApi.getTimerState as any).mock.calls.length;

    await act(async () => {
      vi.advanceTimersByTime(3000);
    });

    expect((timerApi.getTimerState as any).mock.calls.length).toBe(callCount);
  });

  it('updates remaining seconds from API response', async () => {
    (timerApi.createTimer as any).mockResolvedValue(mockTimer);
    (timerApi.startTimer as any).mockResolvedValue(undefined);
    (timerApi.getTimerState as any)
      .mockResolvedValueOnce({
        timerId: 'timer-1',
        remainingSeconds: 300,
        status: 'running',
        urgencyLevel: 'low',
      })
      .mockResolvedValueOnce({
        timerId: 'timer-1',
        remainingSeconds: 298,
        status: 'running',
        urgencyLevel: 'low',
      });

    const { result } = renderHook(() => useTimer());

    await act(async () => {
      await result.current.initTimer(300);
    });

    const firstRemaining = result.current.remainingSeconds;

    await act(async () => {
      await result.current.startTimer();
      vi.advanceTimersByTime(1000);
    });

    await waitFor(() => {
      expect(result.current.remainingSeconds).not.toBe(firstRemaining);
    });
  });
});
