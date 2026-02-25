import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { renderHook, act, waitFor } from '@testing-library/react';
import { useTimer } from '../hooks/useTimer';
import * as timerApi from '../api/timerApi';

vi.mock('../api/timerApi');

describe('useTimer hook', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.runOnlyPendingTimers();
    vi.useRealTimers();
  });

  it('initializes timer on mount', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'active',
      initial_seconds: 30,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockResolvedValue(mockTimer);

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(timerApi.createTimer).toHaveBeenCalledWith(30);
    });

    expect(result.current.timerId).toBe('timer-1');
  });

  it('polls timer state every 1000ms', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'active',
      initial_seconds: 30,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockResolvedValue(mockTimer);

    renderHook(() => useTimer());

    await waitFor(() => {
      expect(timerApi.getTimerState).toHaveBeenCalled();
    });

    const initialCallCount = vi.mocked(timerApi.getTimerState).mock.calls.length;

    act(() => {
      vi.advanceTimersByTime(1000);
    });

    await waitFor(() => {
      expect(vi.mocked(timerApi.getTimerState).mock.calls.length).toBeGreaterThan(initialCallCount);
    });
  });

  it('calls start endpoint when start is invoked', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'paused',
      initial_seconds: 30,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.startTimer).mockResolvedValue({ ...mockTimer, status: 'active' });

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(result.current.timerId).toBe('timer-1');
    });

    await act(async () => {
      await result.current.start();
    });

    expect(timerApi.startTimer).toHaveBeenCalledWith('timer-1');
  });

  it('calls pause endpoint when pause is invoked', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'active',
      initial_seconds: 30,
      remaining_seconds: 25,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.pauseTimer).mockResolvedValue({ ...mockTimer, status: 'paused' });

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(result.current.timerId).toBe('timer-1');
    });

    await act(async () => {
      await result.current.pause();
    });

    expect(timerApi.pauseTimer).toHaveBeenCalledWith('timer-1');
  });

  it('calls reset endpoint when reset is invoked', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'active',
      initial_seconds: 30,
      remaining_seconds: 15,
      urgency_level: 'medium',
    };

    const resetTimer = {
      ...mockTimer,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.resetTimer).mockResolvedValue(resetTimer);

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(result.current.timerId).toBe('timer-1');
    });

    await act(async () => {
      await result.current.reset();
    });

    expect(timerApi.resetTimer).toHaveBeenCalledWith('timer-1');
  });

  it('updates timerState from polling response', async () => {
    const initialTimer = {
      id: 'timer-1',
      status: 'paused',
      initial_seconds: 30,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    const updatedTimer = {
      ...initialTimer,
      remaining_seconds: 25,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(initialTimer);
    vi.mocked(timerApi.getTimerState)
      .mockResolvedValueOnce(initialTimer)
      .mockResolvedValueOnce(updatedTimer);

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(result.current.timerState?.remaining_seconds).toBe(30);
    });

    act(() => {
      vi.advanceTimersByTime(1000);
    });

    await waitFor(() => {
      expect(result.current.timerState?.remaining_seconds).toBe(25);
    });
  });

  it('tracks isRunning state based on status', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'paused',
      initial_seconds: 30,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockResolvedValue(mockTimer);

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(result.current.isRunning).toBe(false);
    });
  });

  it('cleans up interval on unmount', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'active',
      initial_seconds: 30,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockResolvedValue(mockTimer);

    const { unmount } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(timerApi.getTimerState).toHaveBeenCalled();
    });

    const callCountBeforeUnmount = vi.mocked(timerApi.getTimerState).mock.calls.length;

    unmount();

    act(() => {
      vi.advanceTimersByTime(2000);
    });

    expect(vi.mocked(timerApi.getTimerState).mock.calls.length).toBe(callCountBeforeUnmount);
  });

  it('handles API errors gracefully during polling', async () => {
    const mockTimer = {
      id: 'timer-1',
      status: 'active',
      initial_seconds: 30,
      remaining_seconds: 30,
      urgency_level: 'low',
    };

    vi.mocked(timerApi.createTimer).mockResolvedValue(mockTimer);
    vi.mocked(timerApi.getTimerState).mockRejectedValue(new Error('Network error'));

    const { result } = renderHook(() => useTimer());

    await waitFor(() => {
      expect(timerApi.getTimerState).toHaveBeenCalled();
    });

    expect(result.current.timerId).toBe('timer-1');
  });
});
